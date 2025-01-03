import os
import glob
from loguru import logger
import pandas as pd
import pyodbc

# Database connection details
DB_CONNECTION_STRING = (
            "Driver={SQL Server};"
            "Server=localhost;"
            "Database=stockscreener;"
            "Trusted_Connection=yes;"
        )


# Path to CSV files
csv_path = r"C:\\dev\\airtable-zennoposter\\apps\\barchart-trading-strategies\\profile\\datas\\*.csv"

def process_files():
    # Get list of CSV files
    csv_files = glob.glob(csv_path)

    if not csv_files:
        print("No CSV files found.")
        return

    try:
        # Connect to the database
        connection = pyodbc.connect(DB_CONNECTION_STRING)
        cursor = connection.cursor()

        for file in csv_files:
            # Extract the symbol (filename without extension)
            symbol = os.path.splitext(os.path.basename(file))[0]
            logger.info(f"Processing symbol: {symbol}")

            # Read the CSV file
            df = pd.read_csv(file)

            for _, row in df.iterrows():
                # Extract and convert data
                composite_indicators = row["Composite Indicators"]
                total_trades = row["Total # Of Trades"].replace(" Trades", "")
                avg_days_trade = row["Avg Days/Trade"].replace(" Days/Trade", "")
                total_profit = row["Total Profit"].replace("$", "").replace(",", "")

                try:
                    # Keep the sign for total_profit_float
                    total_profit_float = float(total_profit)
                except ValueError:
                    total_profit_float = None

                # SQL Query to update the table
                query = """
                UPDATE bc_stocks_screener
                SET 
                    bc_ts_composite_indicators = ?,
                    bc_ts_total_nb_of_trades = ?,
                    bc_ts_avg_days_trade = ?,
                    bc_ts_total_profit = ?,
                    bc_ts_total_profit_float = ?
                WHERE symbol = ?
                """
                
                # Execute the query
                cursor.execute(query, 
                               composite_indicators, 
                               total_trades, 
                               avg_days_trade, 
                               total_profit, 
                               total_profit_float, 
                               symbol)

        # Commit the transaction
        connection.commit()
        print("Data updated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the connection
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    process_files()
