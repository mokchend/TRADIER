# Example: api/marketdata.py
from loguru import logger
from api.fileutils import save_json
import config
import requests
from datetime import datetime

# https://documentation.tradier.com/brokerage-api/markets/get-options-chains
def get_mktdata_option_chains(symbol='VXX', expiration='2019-05-17'):
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
        return response.json()
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
        
        jsonResponse = response.json()
        # logger.debug(f"Account Positions: {json.dumps(account_positions, indent=4)}")
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/marketdata/{current_datetime}-lookup_options_symbols.json"
        logger.debug(f"Saving get_marketdata_lookup_options_symbols to: {fileName}")
        save_json(jsonResponse, fileName)            
        
        logger.warning("Lookup options symbol retrieved successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching lookup options symbol: {e}")
        return None    