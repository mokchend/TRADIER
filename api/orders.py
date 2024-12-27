# Example: api/orders.py
from loguru import logger
import config
import requests
from datetime import datetime
from api.fileutils import save_json
import inspect

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
        
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/account/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        
        return jsonResponse
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
        
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/account/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        
        return jsonResponse
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching orders: {e}")
        return None
