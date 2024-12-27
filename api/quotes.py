# Example: api/quotes.py
from loguru import logger
import config
import requests

def get_market_quotes(symbol):
    url = f"{config.API_BASE_URL}markets/quotes"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, params={'symbols': symbol}, headers=headers)
        response.raise_for_status()
        logger.info("Market quotes retrieved successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching market quotes: {e}")
        return None