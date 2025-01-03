# Main script: main.py
import json

from loguru import logger
from api.mssqlserver import close_connection, symbolsToStream
import config
import requests
from api import (
    get_market_quotes,
    get_option_chains,
    place_order,
    get_orders,
    get_account_cost_basis,
    get_account_cost_basis_summary,
    get_marketdata_option_chains,
    get_marketdata_lookup_options_symbols,
    get_account_positions,
    get_account_orders,
    get_marketdata_quotes,
    save_json, 
    place_equity_order,
    load_config,
    create_market_session,
    get_market_events
)
import pyodbc

environment = "production1"  # Change this based on your test

# Load configuration
config = load_config(environment)

conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=localhost;"
    "Database=stockscreener;"
    "Trusted_Connection=yes;"
)

# Define headers and payload for the Tradier API request
headers = {
    'Accept': 'application/json'
}

symbols = symbolsToStream(conn)
# return a string of symbols seperated by comma
symbols = ",".join(symbols)
print(f"Symbols: {symbols}")

payload = { 
    'sessionid': f'{create_market_session(config)}',
    'symbols': symbols,
    'linebreak': True,
    'filter': 'trade'
}

# Initialize an empty list for storing processed data
data_stream = []

# Function to process streamed data and append it to the data_stream
def process_stream_data(stream_line):
    try:
        # {"type":"trade","symbol":"TSLA","exch":"Q","price":"379.28","size":"4463367","cvol":"109710749","date":"1735851600072","last":"379.28"}
        
        # Parse the JSON line
        event = json.loads(stream_line)
        
        # Extract relevant fields (example assumes 'price', 'volume', and 'timestamp' keys exist)
        # Adjust field names as per the actual API response
        type = event.get('type', 'UNKNOWN')
        symbol = event.get('symbol', 'UNKNOWN')
        exch = event.get('exch', 'UNKNOWN')
        price = event.get('price', 0.0)
        size = event.get('size', 0)
        cvol = event.get('cvol', 0)
        date = event.get('date', None)
        last = event.get('last', 0.0)

        # Append the processed record to the data_stream
        data_stream.append((type, symbol, exch, price, size, cvol, date, last))

        # Print to confirm processing (optional)
        # print(f"Processed: {symbol}, {price}, {volume}, {timestamp}")
    except Exception as e:
        # Handle errors (e.g., invalid JSON or missing keys)
        print(f"Error processing stream line: {e}")


def save_to_database(conn, data):
    try:
        print(f"Saving {len(data)} records to the database")
        print(data)
        cursor = conn.cursor()
        # Upsert data into StockPrices table
        query = """
            MERGE td_stock_prices AS target
            USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?)) AS source (type, symbol, exch, price, size, cvol, date, last)
            ON target.symbol = source.symbol
            WHEN MATCHED THEN 
                UPDATE SET type = source.type, exch = source.exch, price = source.price, size = source.size, cvol = source.cvol, date = source.date, last = source.last, last_update_date = SYSDATETIME()
            WHEN NOT MATCHED THEN
                INSERT (type, symbol, exch, price, size, cvol, date, last, last_update_date)
                VALUES (source.type, source.symbol, source.exch, source.price, source.size, source.cvol, source.date, source.last, SYSDATETIME());
        """
        cursor.executemany(query, data)
        conn.commit()
    except Exception as e:
        logger.error(f"Error saving data to database: {e}")

# Example usage with streamed data
# data_stream = [
#     ("AAPL", 175.23, 1000, "2025-01-03 14:30:00"),
#     ("GOOGL", 2849.56, 150, "2025-01-03 14:30:00"),
#     # Add more rows as needed
# ]

# save_to_database(data_stream)



# Make the request to the Tradier streaming API
r = requests.get('https://stream.tradier.com/v1/markets/events', stream=True, params=payload, headers=headers)

try:
    # Iterate over the streamed lines
    for line in r.iter_lines():
        if line:
            decoded_line = line.decode('utf-8')
            print(decoded_line)
            process_stream_data(decoded_line)  # Decode bytes to string before processing
            save_to_database(conn, data_stream)
            # exit(0)
except KeyboardInterrupt:
    print("\nLoop interrupted by user. Exiting gracefully.")
finally:
    close_connection(conn)
# After the loop ends, data_stream contains all processed records



