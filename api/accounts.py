# Example: api/quotes.py
import json
from loguru import logger
from api.mssqlserver import upsert_account_orders, upsert_account_positions, upsert_account_orders
import requests

from datetime import datetime
from api.fileutils import save_json
import inspect


# https://documentation.tradier.com/brokerage-api/trading/place-equity-order
def place_equity_order(config, order_type='limit', symbol='FTNT', quantity='10.00', side='buy', duration='gtc', price='1.00', stop=None):
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/orders"
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    function_name = inspect.currentframe().f_code.co_name
        
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    order_data = {
        'class': 'equity',
        'symbol': f'{symbol}',
        'duration': f'{duration}',
        'side': f'{side}',
        'quantity': f'{quantity}',
        'type': f'{order_type}'
    }
    if price:
        order_data['price'] = f'{price}'
    if stop:
        order_data['stop'] = f'{stop}'
    
    try:
        
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/account/{current_datetime}_{function_name}_request.json"
        save_json(order_data, fileName)
        logger.debug(f"Order data being sent: {json.dumps(order_data, indent=2)}")

        logger.warning(f"Request URL: {url}")
        logger.warning(f"Headers: {headers}")
        logger.warning(f"Payload: {order_data}")        
        

        response = requests.post(url, headers=headers, data=order_data)
        response.raise_for_status()
        logger.info("Equity order placed successfully.")
        
         
        
        jsonResponse = response.json()
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/account/{current_datetime}_{function_name}_response.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)
        
        return jsonResponse
    # except requests.exceptions.RequestException as e:
    #     logger.error(f"Error placing equity order: {e}")
    #     return None
    except requests.exceptions.HTTPError as http_err:
        error_details = http_err.response.text
        logger.error(f"Error placing equity order: {error_details}")    
        return None

# https://documentation.tradier.com/brokerage-api/accounts/get-account-orders
def get_account_orders():
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/orders"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    params={}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        logger.info("Get an account’s orders retrieved successfully.")
        
        
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/account/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        
        upsert_account_orders(fileName)
        
        return jsonResponse
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Get an account’s orders: {e}")
        return None


# https://documentation.tradier.com/brokerage-api/accounts/get-account-positions
def get_account_positions():
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/positions"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    params = {}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        logger.info("Get an account’s positions retrieved successfully.")
            
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/account/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)  
        
        upsert_account_positions(fileName)    
        
        return jsonResponse
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Get an account’s positions: {e}")
        return None

# https://documentation.tradier.com/brokerage-api/accounts/get-account-gainloss

def get_account_cost_basis_summary():
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/gainloss"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    params = {
        'page': '3',
        'limit': '100',
        'sortBy': 'closeDate',
        'sort': 'desc'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        logger.info("Get an account’s cost basis retrieved successfully.")
        
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/account/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        
        return jsonResponse
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching an account’s cost basis: {e}")
        return None

def get_account_cost_basis(symbol):
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/gainloss"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    params = {
        'page': '3',
        'limit': '100',
        'sortBy': 'closeDate',
        'sort': 'desc',
        # 'start': 'yyyy-mm-dd',
        # 'end': 'yyyy-mm-dd',
        'symbol': symbol
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        logger.info("Get an account’s cost basis retrieved successfully.")
        
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/account/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        
        return jsonResponse
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching an account’s cost basis: {e}")
        return None