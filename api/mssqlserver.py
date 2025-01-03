import json
from loguru import logger
import pyodbc
from datetime import datetime
from api.fileutils import save_json
import inspect


conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=localhost;"
    "Database=stockscreener;"
    "Trusted_Connection=yes;"
)

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


def create_connection(server, database, trusted_connection=True, username=None, password=None):
    """
    Establishes a connection to the SQL Server.
    """
    try:
        if trusted_connection:
            conn = pyodbc.connect(
                f"Driver={{SQL Server}};"
                f"Server={server};"
                f"Database={database};"
                f"Trusted_Connection=yes;"
            )
        else:
            conn = pyodbc.connect(
                f"Driver={{SQL Server}};"
                f"Server={server};"
                f"Database={database};"
                f"UID={username};"
                f"PWD={password};"
            )
        return conn
    except pyodbc.Error as e:
        print(f"Error: {e}")
        return None

def execute_query(conn, query):
    """
    Executes a given query on the provided connection and fetches the results.
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except pyodbc.Error as e:
        print(f"Error executing query: {e}")
        return None

def close_connection(conn):
    """
    Closes the database connection.
    """
    try:
        conn.close()
        print("Connection closed successfully.")
    except pyodbc.Error as e:
        print(f"Error closing connection: {e}")

def upsert_account_positions(jsonFile):

    # Load the JSON data
    with open(jsonFile, 'r') as file:
        data = json.load(file)

    positions = data['positions']['position']

    # Connect to the database
    try:
        connection = pyodbc.connect(
            "Driver={SQL Server};"
            "Server=localhost;"
            "Database=stockscreener;"
            "Trusted_Connection=yes;"
        )
        cursor = connection.cursor()

        # Separate SQL queries for insert and update
        update_query = """
        UPDATE stockscreener.dbo.td_position
        SET id_position = ?, quantity = ?, cost_basis = ?, date_acquired = ?
        WHERE symbol = ?;
        """

        insert_query = """
        INSERT INTO stockscreener.dbo.td_position (symbol, id_position, quantity, cost_basis, date_acquired)
        VALUES (?, ?, ?, ?, ?);
        """

        # Process each position in the JSON file
        for position in positions:
            params = (
                position['id'],
                position['quantity'],
                position['cost_basis'],
                datetime.fromisoformat(position['date_acquired'].replace('Z', '+00:00')),
                position['symbol']
            )

            # Attempt to update first
            cursor.execute(update_query, params)

            # Check if update affected any rows; if not, insert
            if cursor.rowcount == 0:
                insert_params = (
                    position['symbol'],
                    position['id'],
                    position['quantity'],
                    position['cost_basis'],
                    datetime.fromisoformat(position['date_acquired'].replace('Z', '+00:00'))
                )
                cursor.execute(insert_query, insert_params)

        # Commit the transaction
        connection.commit()
        print("Upsert operation completed successfully.")

    except pyodbc.Error as e:
        print(f"Database error occurred: {e}")
    finally:
        # Close the connection
        if 'connection' in locals() and connection:
            connection.close()

def upsert_account_orders(jsonFile):

    # Load the JSON data
    with open(jsonFile, 'r') as file:
        data = json.load(file)

    # Connect to the database
    try:
        connection = pyodbc.connect(
            "Driver={SQL Server};"
            "Server=localhost;"
            "Database=stockscreener;"
            "Trusted_Connection=yes;"
        )
        cursor = connection.cursor()

        # Separate SQL queries for insert and update for orders
        update_order_query = """
        UPDATE td_orders
        SET type = ?, symbol = ?, side = ?, quantity = ?, status = ?, duration = ?, price = ?,
            avg_fill_price = ?, exec_quantity = ?, last_fill_price = ?, last_fill_quantity = ?, remaining_quantity = ?,
            create_date = ?, transaction_date = ?, class = ?, num_legs = ?, strategy = ?
        WHERE id = ?;
        """

        insert_order_query = """
        INSERT INTO td_orders (id, type, symbol, side, quantity, status, duration, price, avg_fill_price, exec_quantity,
                               last_fill_price, last_fill_quantity, remaining_quantity, create_date, transaction_date, class, num_legs, strategy)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        # Separate SQL queries for insert and update for legs
        update_leg_query = """
        UPDATE td_legs
        SET order_id = ?, type = ?, symbol = ?, side = ?, quantity = ?, status = ?, duration = ?, price = ?,
            avg_fill_price = ?, exec_quantity = ?, last_fill_price = ?, last_fill_quantity = ?, remaining_quantity = ?,
            create_date = ?, transaction_date = ?, class = ?, option_symbol = ?
        WHERE id = ?;
        """

        insert_leg_query = """
        INSERT INTO td_legs (id, order_id, type, symbol, side, quantity, status, duration, price, avg_fill_price,
                             exec_quantity, last_fill_price, last_fill_quantity, remaining_quantity, create_date,
                             transaction_date, class, option_symbol)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
        """

        # Iterate through orders and legs
        for order in data["orders"]["order"]:
            order_params = (
                order["type"], order["symbol"], order["side"], order["quantity"], order["status"], order["duration"],
                order.get("price", 0)  , order["avg_fill_price"], order["exec_quantity"], order["last_fill_price"],
                order["last_fill_quantity"], order["remaining_quantity"], order["create_date"], order["transaction_date"],
                order["class"], order.get("num_legs"), order.get("strategy"), order["id"]
            )

            # Attempt to update first
            cursor.execute(update_order_query, order_params)

            # Check if update affected any rows; if not, insert
            if cursor.rowcount == 0:
                insert_order_params = (
                    order["id"], order["type"], order["symbol"], order["side"], order["quantity"], order["status"],
                    order["duration"], order.get("price", 0), order["avg_fill_price"], order["exec_quantity"],
                    order["last_fill_price"], order["last_fill_quantity"], order["remaining_quantity"],
                    order["create_date"], order["transaction_date"], order["class"], order.get("num_legs"),
                    order.get("strategy")
                )
                cursor.execute(insert_order_query, insert_order_params)

            for leg in order.get("leg", []):
                leg_params = (
                    order["id"], leg["type"], leg["symbol"], leg["side"], leg["quantity"], leg["status"],
                    leg["duration"], leg.get("price",0), leg["avg_fill_price"], leg["exec_quantity"], leg["last_fill_price"],
                    leg["last_fill_quantity"], leg["remaining_quantity"], leg["create_date"], leg["transaction_date"],
                    leg["class"], leg.get("option_symbol"), leg["id"]
                )

                # Attempt to update first
                cursor.execute(update_leg_query, leg_params)

                # Check if update affected any rows; if not, insert
                if cursor.rowcount == 0:
                    insert_leg_params = (
                        leg["id"], order["id"], leg["type"], leg["symbol"], leg["side"], leg["quantity"],
                        leg["status"], leg["duration"], leg.get("price",0), leg["avg_fill_price"], leg["exec_quantity"],
                        leg["last_fill_price"], leg["last_fill_quantity"], leg["remaining_quantity"], leg["create_date"],
                        leg["transaction_date"], leg["class"], leg.get("option_symbol")
                    )
                    cursor.execute(insert_leg_query, insert_leg_params)

        # Commit the transaction
        connection.commit()

    except pyodbc.Error as e:
        print(f"Database error occurred: {e}")
    finally:
        cursor.close()
        # Close the connection
        if 'connection' in locals() and connection:
            connection.close()
