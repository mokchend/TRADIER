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


def upsert_account_position(jsonfFileAccountPositions):
    
    # Load the JSON data
    with open(jsonfFileAccountPositions, 'r') as file:
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
