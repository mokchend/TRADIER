# Example: api/orders.py
from loguru import logger
import config
import requests

def place_order(symbol, option_symbol, quantity):
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/orders"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    data = {
        'class': 'option', 
        'symbol': symbol, 
        'option_symbol': option_symbol, 
        'side': 'buy_to_open', 
        'quantity': str(quantity), 
        'type': 'market', 
        'duration': 'day'
    }
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        logger.info("Order placed successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error placing order: {e}")
        return None

def get_orders():
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/orders"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.warning("Orders retrieved successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching orders: {e}")
        return None
