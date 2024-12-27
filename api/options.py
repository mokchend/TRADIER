# Example: api/options.py
from loguru import logger
import config
import requests

def get_option_chains(symbol, expiration):
    url = f"{config.API_BASE_URL}markets/options/chains"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, params={'symbol': symbol, 'expiration': expiration}, headers=headers)
        response.raise_for_status()
        logger.info("Option chains retrieved successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching option chains: {e}")
        return None