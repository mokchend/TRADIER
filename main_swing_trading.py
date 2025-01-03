# Main script: main.py
import json
from api.mssqlserver import close_connection
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

from loguru import logger
import json
import pyodbc
from datetime import datetime
from api.fileutils import save_json
import inspect
from datetime import datetime

conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=localhost;"
    "Database=stockscreener;"
    "Trusted_Connection=yes;"
)


def buy_at_market_price(conn, symbol):
    """
    Executes a given query on the provided connection and fetches the results.
    """
    query_buy = f"""
        SELECT TOP 1 created_date, account_name, symbol, quantity_buy, price_buy, cpt_buy, cpt_max_buy
        FROM td_swing_trading tst
        WHERE 
            trade_status_buy = 'In progress' AND symbol = '{symbol}'
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query_buy)
        
        # Fetch the result
        row = cursor.fetchone()
        if row:
            # Access results by column name
            result = {
                "created_date": row.created_date,
                "account_name": row.account_name,
                "symbol": row.symbol,
                "quantity_buy": row.quantity_buy,
                "price_buy": row.price_buy,
                "cpt_buy": row.cpt_buy,
                "cpt_max_buy": row.cpt_max_buy
            }
            logger.info(f"BUY Results: {result}")
            account_name = result.get('account_name')
            symbol = result.get('symbol')
            
            quantity_buy = result.get('quantity_buy')
            price_buy = result.get('price_buy')
            
            # cpt_buy = result.get('cpt_buy')
            # cpt_max_buy = result.get('cpt_max_buy')
            created_date = result.get('created_date')
            
            # cpt_buy += 1
            # add a condition to buy at market price
            # price_hack = 
            logger.warning(f"BUY {symbol} : price_buy={price_buy} > price={price} ?")
            if ( price_buy > float(price) ):
                # TODO : OK to buy at market price, place order and update the trade status
                logger.warning(f"OK to BUY at market price: {price}")
                
                # Get current date and time
                current_datetime = datetime.now()
                
                # Define the parameterized update query
                update_query = f"""
                    UPDATE td_swing_trading
                    SET 
                        cpt_max_buy = 0,
                        date_buy = ?,                        
                        trade_status_buy = 'Completed'
                    WHERE 
                         created_date = ? AND symbol = ? AND account_name = ?
                """

                # Execute the update query with parameters
                cursor.execute(update_query, current_datetime, created_date, symbol, account_name)
                
                # Commit the changes
                conn.commit()

                logger.warning(f"Record for symbol '{symbol}' updated successfully.")                
                # exit(0)
            
        else:
            logger.debug(f"No swing trade configuration for symbol '{symbol}'")
            
        cursor.close()
    except pyodbc.Error as e:
        print(f"Error executing query: {e}")
        # return None


def sell_at_market_price(conn, symbol):
    """
    Executes a given query on the provided connection and fetches the results.
    """
    query_sell = f"""
        SELECT TOP 1 created_date, account_name, symbol, quantity_sell, price_sell, cpt_sell, cpt_max_sell
        FROM td_swing_trading tst
        WHERE 
            trade_status_buy = 'Completed' AND trade_status_sell = 'In progress' AND symbol = '{symbol}'
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query_sell)
        
        # Fetch the result
        row = cursor.fetchone()
        if row:
            # Access results by column name
            result = {
                "created_date": row.created_date,
                "account_name": row.account_name,
                "symbol": row.symbol,
                "quantity_sell": row.quantity_sell,
                "price_sell": row.price_sell,
                "cpt_sell": row.cpt_sell,
                "cpt_max_sell": row.cpt_max_sell
            }
            logger.info(f"SELL Results: {result}")
            account_name = result.get('account_name')
            symbol = result.get('symbol')
            
            quantity_sell = result.get('quantity_sell')
            price_sell = result.get('price_sell')
            
            # cpt_sell = result.get('cpt_sell')
            # cpt_max_sell = result.get('cpt_max_sell')
            created_date = result.get('created_date')
            
            # cpt_sell += 1
            # add a condition to sell at market price
            # price_hack = 
            logger.warning(f"SELL {symbol} : price_sell={price_sell} < price={price} ?")
            if ( price_sell < float(price) ):
                # TODO : OK to sell at market price, place order and update the trade status
                logger.warning(f"OK to SELL at market price: {price}")
                
                # Get current date and time
                current_datetime = datetime.now()
                
                # Define the parameterized update query
                update_query = f"""
                    UPDATE td_swing_trading
                    SET 
                        date_sell = ?,                        
                        trade_status_sell = 'Completed'
                    WHERE 
                         created_date = ? AND symbol = ? AND account_name = ?
                """

                # Execute the update query with parameters
                cursor.execute(update_query, current_datetime, created_date, symbol, account_name)
                
                # Commit the changes
                conn.commit()

                logger.warning(f"Record for SELL symbol '{symbol}' updated successfully.")                
                # exit(0)
            
        else:
            logger.debug(f"No swing trade configuration for symbol '{symbol}'")
            
        cursor.close()
    except pyodbc.Error as e:
        print(f"Error executing query: {e}")
        # return None


def symbolsToStream(conn):
    """
    Executes a given query on the provided connection and fetches the results.
    """
    query_symbols = f"""
        select distinct symbol
        from td_swing_trading tst 
    """
    
    symbols = []
    
    try:
        cursor = conn.cursor()
        cursor.execute(query_symbols)
        
        # Fetch the result
        rows = cursor.fetchall()
        if rows:
            # Access results by column name
            for row in rows:
                symbol = row.symbol
                symbols.append(symbol)
        else:
            logger.debug(f"No symbols found")
            
        cursor.close()
        print(f"Symbols: {symbols}")
        return symbols
    except pyodbc.Error as e:
        print(f"Error executing query: {e}")
        return []



if __name__ == "__main__":
    logger.info("Starting API interactions...")
    # Define the environment: 'sandbox', 'production1', 'production2'
    environment = "production1"  # Change this based on your test

    # Load configuration
    config = load_config(environment)

    headers = {
        'Accept': 'application/json'
    }
    
    symbols = symbolsToStream(conn)
    # return a string of symbols seperated by comma
    symbols = ",".join(symbols)
    print(f"Symbols: {symbols}")

    payload = { 
        'sessionid': f'{create_market_session(config)}',
        'symbols': symbols, #, MSTR, CRM
        'linebreak': True
    }


# {
#     'type': 'trade', 
#     'symbol': 'MSTR', 
#     'exch': 'Q', 
#     'price': '289.62', 
#     'size': '1184593', 
#     'cvol': '1144373', 
#     'date': '1735678800174', 
#     'last': '289.62'
# }

    cpt = 0
    cpt_max = 50
    r = requests.get('https://stream.tradier.com/v1/markets/events', stream=True, params=payload, headers=headers)
    for line in r.iter_lines():
        if line:
            # print(json.loads(line))
            # logger.info(line)
            # Example byte string
            byte_data = line
            # Decode to string
            decoded_string = byte_data.decode('utf-8')
                    
            # Parse as JSON
            parsed_data = json.loads(decoded_string)
            # logger.warning(f"{parsed_data}")
            price = parsed_data.get('price')
            last = parsed_data.get('last')
            symbol = parsed_data.get('symbol')
            # logger.warning(f"Price: {price}, Last: {last}")
            if (price!=None and last!=None):
                if (price==last):
                    logger.info(f"Symbol: {symbol} Price: {price}")
                    # break
                    buy_at_market_price(conn, symbol)
                    # sell_at_market_price(conn, symbol)
                    
    close_connection(conn)
    