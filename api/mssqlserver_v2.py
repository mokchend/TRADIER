import json
import pyodbc
from datetime import datetime
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
        USING (SELECT :symbol AS symbol, :id_position AS id_position, :quantity AS quantity, :cost_basis AS cost_basis, :date_acquired AS date_acquired) AS source
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
            params = {
                'symbol': position['symbol'],
                'id_position': position['id'],
                'quantity': position['quantity'],
                'cost_basis': position['cost_basis'],
                'date_acquired': datetime.fromisoformat(position['date_acquired'].replace('Z', '+00:00'))
            }

            # Execute the upsert query
            cursor.execute(upsert_query, params)

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
        USING (VALUES (:id, :type, :symbol, :side, :quantity, :status, :duration, :price, :avg_fill_price, :exec_quantity, :last_fill_price, :last_fill_quantity, :remaining_quantity, :create_date, :transaction_date, :class, :num_legs, :strategy)) AS source
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
        USING (VALUES (:id, :order_id, :type, :symbol, :side, :quantity, :status, :duration, :price, :avg_fill_price, :exec_quantity, :last_fill_price, :last_fill_quantity, :remaining_quantity, :create_date, :transaction_date, :class, :option_symbol)) AS source
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
            order_params = {
                'id': order.get("id", None),
                'type': order.get("type", None),
                'symbol': order.get("symbol", None),
                'side': order.get("side", None),
                'quantity': order.get("quantity", None),
                'status': order.get("status", None),
                'duration': order.get("duration", None),
                'price': order.get("price", None),
                'avg_fill_price': order.get("avg_fill_price", None),
                'exec_quantity': order.get("exec_quantity", None),
                'last_fill_price': order.get("last_fill_price", None),
                'last_fill_quantity': order.get("last_fill_quantity", None),
                'remaining_quantity': order.get("remaining_quantity", None),
                'create_date': order.get("create_date", None),
                'transaction_date': order.get("transaction_date", None),
                'class': order.get("class", None),
                'num_legs': order.get("num_legs", 0),
                'strategy': order.get("strategy", None)
            }
            
            print("Executing Query:", order_query)
            print("With Parameters:", order_params)


            cursor.execute(order_query, order_params)

            for leg in order.get("leg", []):
                leg_params = {
                    'id': leg.get("id", None),
                    'order_id': order.get("id", None),
                    'type': leg.get("type", None),
                    'symbol': leg.get("symbol", None),
                    'side': leg.get("side", None),
                    'quantity': leg.get("quantity", None),
                    'status': leg.get("status", None),
                    'duration': leg.get("duration", None),
                    'price': leg.get("price", None),
                    'avg_fill_price': leg.get("avg_fill_price", None),
                    'exec_quantity': leg.get("exec_quantity", None),
                    'last_fill_price': leg.get("last_fill_price", None),
                    'last_fill_quantity': leg.get("last_fill_quantity", None),
                    'remaining_quantity': leg.get("remaining_quantity", None),
                    'create_date': leg.get("create_date", None),
                    'transaction_date': leg.get("transaction_date", None),
                    'class': leg.get("class", None),
                    'option_symbol': leg.get("option_symbol", None)
                }

                cursor.execute(leg_query, leg_params)

        # Commit and close
        connection.commit()

    except pyodbc.Error as e:
        print(f"Database error occurred: {e}")
        # print(inspect.stack()[0][3])
        # print stack trace
        print(inspect.stack())
    finally:
        cursor.close()
        # Close the connection
        if 'connection' in locals() and connection:
            connection.close()
