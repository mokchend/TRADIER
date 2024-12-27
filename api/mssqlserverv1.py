import json
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

        # SQL query for upsert
        upsert_query = """
        MERGE INTO stockscreener.dbo.td_position AS target
        USING (SELECT ? AS symbol, ? AS id_position, ? AS quantity, ? AS cost_basis, ? AS date_acquired) AS source
        ON target.symbol = source.symbol
        WHEN MATCHED THEN
            UPDATE SET id_position = source.id_position, 
                    quantity = source.quantity, 
                    cost_basis = source.cost_basis, 
                    date_acquired = source.date_acquired
        WHEN NOT MATCHED THEN
            INSERT (symbol, id_position, quantity, cost_basis, date_acquired)
            VALUES (source.symbol, source.id_position, source.quantity, source.cost_basis, source.date_acquired);
        """

        # Process each position in the JSON file
        for position in positions:
            symbol = position['symbol']
            id_position = position['id']
            quantity = position['quantity']
            cost_basis = position['cost_basis']
            date_acquired = datetime.fromisoformat(position['date_acquired'].replace('Z', '+00:00'))

            # Execute the upsert query
            cursor.execute(upsert_query, (symbol, id_position, quantity, cost_basis, date_acquired))

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

        # Upsert td_orders
        order_query = """
        MERGE INTO td_orders AS target
        USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source
        (id, type, symbol, side, quantity, status, duration, price, avg_fill_price, exec_quantity, last_fill_price, last_fill_quantity, remaining_quantity, create_date, transaction_date, class, num_legs, strategy)
        ON target.id = source.id
        WHEN MATCHED THEN
            UPDATE SET type = source.type, symbol = source.symbol, side = source.side, quantity = source.quantity, status = source.status,
            duration = source.duration, price = source.price, avg_fill_price = source.avg_fill_price, exec_quantity = source.exec_quantity,
            last_fill_price = source.last_fill_price, last_fill_quantity = source.last_fill_quantity, remaining_quantity = source.remaining_quantity,
            create_date = source.create_date, transaction_date = source.transaction_date, class = source.class, num_legs = source.num_legs,
            strategy = source.strategy
        WHEN NOT MATCHED THEN
            INSERT (id, type, symbol, side, quantity, status, duration, price, avg_fill_price, exec_quantity, last_fill_price, last_fill_quantity, remaining_quantity, create_date, transaction_date, class, num_legs, strategy)
            VALUES (source.id, source.type, source.symbol, source.side, source.quantity, source.status, source.duration, source.price, source.avg_fill_price, source.exec_quantity, source.last_fill_price, source.last_fill_quantity, source.remaining_quantity, source.create_date, source.transaction_date, source.class, source.num_legs, source.strategy);
        """

        leg_query = """
        MERGE INTO td_legs AS target
        USING (VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)) AS source
        (id, order_id, type, symbol, side, quantity, status, duration, price, avg_fill_price, exec_quantity, last_fill_price, last_fill_quantity, remaining_quantity, create_date, transaction_date, class, option_symbol)
        ON target.id = source.id
        WHEN MATCHED THEN
            UPDATE SET order_id = source.order_id, type = source.type, symbol = source.symbol, side = source.side, quantity = source.quantity,
            status = source.status, duration = source.duration, price = source.price, avg_fill_price = source.avg_fill_price, exec_quantity = source.exec_quantity,
            last_fill_price = source.last_fill_price, last_fill_quantity = source.last_fill_quantity, remaining_quantity = source.remaining_quantity,
            create_date = source.create_date, transaction_date = source.transaction_date, class = source.class, option_symbol = source.option_symbol
        WHEN NOT MATCHED THEN
            INSERT (id, order_id, type, symbol, side, quantity, status, duration, price, avg_fill_price, exec_quantity, last_fill_price, last_fill_quantity, remaining_quantity, create_date, transaction_date, class, option_symbol)
            VALUES (source.id, source.order_id, source.type, source.symbol, source.side, source.quantity, source.status, source.duration, source.price, source.avg_fill_price, source.exec_quantity, source.last_fill_price, source.last_fill_quantity, source.remaining_quantity, source.create_date, source.transaction_date, source.class, source.option_symbol);
        """

        # Iterate through orders and legs
        for order in data["orders"]["order"]:
            cursor.execute(order_query, (
                order["id"], order["type"], order["symbol"], order["side"], order["quantity"], order["status"], order["duration"], order["price"],
                order["avg_fill_price"], order["exec_quantity"], order["last_fill_price"], order["last_fill_quantity"], order["remaining_quantity"],
                order["create_date"], order["transaction_date"], order["class"], order.get("num_legs"), order.get("strategy")
            ))
            
            for leg in order.get("leg", []):
                cursor.execute(leg_query, (
                    leg["id"], order["id"], leg["type"], leg["symbol"], leg["side"], leg["quantity"], leg["status"], leg["duration"], leg["price"],
                    leg["avg_fill_price"], leg["exec_quantity"], leg["last_fill_price"], leg["last_fill_quantity"], leg["remaining_quantity"],
                    leg["create_date"], leg["transaction_date"], leg["class"], leg.get("option_symbol")
                ))

        # Commit and close
        connection.commit()        
        

    except pyodbc.Error as e:
        print(f"Database error occurred: {e}")
    finally:
        cursor.close()
        # Close the connection
        if 'connection' in locals() and connection:
            connection.close()
