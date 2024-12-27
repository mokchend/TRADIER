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



