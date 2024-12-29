# Example: api/quotes.py
import json
from loguru import logger
from api.mssqlserver import upsert_account_orders, upsert_account_positions, upsert_account_orders
import config
import requests

from datetime import datetime
from api.fileutils import save_json
import inspect



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