# Example: api/quotes.py
import json
from loguru import logger
import config
import requests
from datetime import datetime

def get_market_quotes(symbol):
    url = f"{config.API_BASE_URL}markets/quotes"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, params={'symbols': symbol}, headers=headers)
        response.raise_for_status()
        logger.warning("Market quotes retrieved successfully.")
        return response.json()
        # return {json.dumps(response.json(), indent=4)}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching market quotes: {e}")
        return None