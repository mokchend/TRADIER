# Example: api/trading.py
import json
from loguru import logger
import config
import requests
from datetime import datetime

# https://documentation.tradier.com/brokerage-api/trading/cancel-order
def cancel_an_order(order_id):
    
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/orders/{order_id}"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    params = {}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        logger.warning("Cancel an Order retrieved successfully.")
        return response.json()
        # return {json.dumps(response.json(), indent=4)}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Cancel an Order: {e}")
        return None