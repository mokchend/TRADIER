# Main script: main.py
import json
from api import (
    create_connection,
    execute_query,
    close_connection
)
from loguru import logger

def main():
    """
    Main function to demonstrate the usage of grouped functions.
    """
    server = "localhost"
    database = "stockscreener"
    query = "SELECT * FROM degiro"
    
    # Create connection
    conn = create_connection(server, database, trusted_connection=True)
    
    if conn:
        # Execute query
        results = execute_query(conn, query)
        if results:
            for row in results:
                print(row)

        # Close connection
        close_connection(conn)


if __name__ == "__main__":
    main()