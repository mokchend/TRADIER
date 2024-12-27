# Example: api/marketdata.py
from loguru import logger
import config
import requests

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
        logger.warning("Lookup options symbol retrieved successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching lookup options symbol: {e}")
        return None    