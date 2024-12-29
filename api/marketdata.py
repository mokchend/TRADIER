# Example: api/marketdata.py
from loguru import logger
from api.fileutils import save_json
import config
import requests
from datetime import datetime
from api.fileutils import save_json
import inspect

# https://documentation.tradier.com/brokerage-api/markets/get-options-chains
def get_marketdata_option_chains(symbol='VXX', expiration='2019-05-17'):
    url = f"{config.API_BASE_URL}markets/options/chains"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    params={'symbol': symbol, 'expiration': expiration, 'greeks': 'true'}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        logger.warning("Option chains retrieved successfully.")
        
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/marketdata/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        
        
        filtered_data = [
            {
                "symbol": option["symbol"],
                "strike": option["strike"],
                "bid": option["bid"],
                "mid": (option["bid"] + option["ask"]) / 2 if option["bid"] is not None and option["ask"] is not None else None,
                "ask": option["ask"],                    
            }
            for option in jsonResponse["options"]["option"]
        ]
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/marketdata/{current_datetime}_{function_name}_FILTERED.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(filtered_data, fileName)      
        
        
        
        return jsonResponse
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching option chains: {e}")
        return None
    
# https://documentation.tradier.com/brokerage-api/markets/get-lookup-options-symbols    
def get_marketdata_lookup_options_symbols(underlying='SPY'):
    url = f"{config.API_BASE_URL}markets/options/lookup"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    params={'underlying': underlying}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
                
        logger.warning("Lookup options symbol retrieved successfully.")
        
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/marketdata/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        
        return jsonResponse
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching lookup options symbol: {e}")
        return None    
    
    
# https://documentation.tradier.com/brokerage-api/markets/get-quotes
def get_marketdata_quotes(symbols='CRM,MSTR'):
    function_name = inspect.currentframe().f_code.co_name
    url = f"{config.API_BASE_URL}markets/quotes"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    params={'symbols': symbols, 'greeks': 'false'}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
                
        logger.warning("{function_name} retrieved successfully.")
        
        jsonResponse = response.json()
        
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/marketdata/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        
        return jsonResponse
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching lookup options symbol: {e}")
        return None        