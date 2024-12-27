# Example: api/trading.py
import json
from loguru import logger
import config
import requests
from datetime import datetime
from api.fileutils import save_json
import inspect
from api.order_params import get_multileg_order_params

# https://documentation.tradier.com/brokerage-api/trading/place-multileg-order
def place_a_multileg_order():
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/orders"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    params = get_multileg_order_params()
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/trading/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        logger.warning("{function_name} retrieved successfully.")
        
        return jsonResponse
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Cancel an Order: {e}")
        return None

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
        
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/account/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        
        return jsonResponse
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Cancel an Order: {e}")
        return None