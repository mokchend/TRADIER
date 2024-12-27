# Example: api/options.py
from loguru import logger
import config
import requests
from datetime import datetime

def get_option_chains(symbol, expiration):
    url = f"{config.API_BASE_URL}markets/options/chains"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, params={'symbol': symbol, 'expiration': expiration}, headers=headers)
        response.raise_for_status()
        logger.warning("Option chains retrieved successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching option chains: {e}")
        return None