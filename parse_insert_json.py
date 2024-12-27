import json
import mysql.connector
from loguru import logger

# JSON data
json_data = """
<Your JSON data here>
"""

# Parse JSON
data = json.loads(json_data)

# Database connection
conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database"
)
cursor = conn.cursor()

# Insert main order data
def insert_orders(data):
    for order in data["orders"]["order"]:
        try:
            query = """
            INSERT INTO td_account_order (
                id, type, symbol, side, quantity, status, duration, price,
                avg_fill_price, exec_quantity, last_fill_price, last_fill_quantity,
                remaining_quantity, create_date, transaction_date, class, strategy, reason_description
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                order["id"], order["type"], order["symbol"], order["side"],
                order["quantity"], order["status"], order["duration"], order["price"],
                order["avg_fill_price"], order["exec_quantity"], order["last_fill_price"],
                order["last_fill_quantity"], order["remaining_quantity"], 
                order["create_date"], order["transaction_date"], 
                order["class"], order.get("strategy"), order.get("reason_description")
            )
            cursor.execute(query, values)
            
            # Insert leg data
            if "leg" in order:
                for leg in order["leg"]:
                    insert_leg(leg, order["id"])
        except Exception as e:
            logger.error(f"Error inserting order {order['id']}: {e}")
            conn.rollback()

# Insert leg data
def insert_leg(leg, order_id):
    try:
        query = """
        INSERT INTO td_account_order_leg (
            id, order_id, type, symbol, side, quantity, status, duration, price,
            avg_fill_price, exec_quantity, last_fill_price, last_fill_quantity,
            remaining_quantity, create_date, transaction_date, class, option_symbol
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            leg["id"], order_id, leg["type"], leg["symbol"], leg["side"],
            leg["quantity"], leg["status"], leg["duration"], leg["price"],
            leg["avg_fill_price"], leg["exec_quantity"], leg["last_fill_price"],
            leg["last_fill_quantity"], leg["remaining_quantity"], 
            leg["create_date"], leg["transaction_date"], 
            leg["class"], leg.get("option_symbol")
        )
        cursor.execute(query, values)
    except Exception as e:
        logger.error(f"Error inserting leg {leg['id']} for order {order_id}: {e}")
        conn.rollback()

# Run insertion
try:
    insert_orders(data)
    conn.commit()
    logger.info("Data inserted successfully.")
except Exception as e:
    logger.error(f"Error during insertion: {e}")
finally:
    cursor.close()
    conn.close()
