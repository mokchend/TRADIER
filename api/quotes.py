# Example: api/quotes.py
import json
from loguru import logger
import config
import requests
from datetime import datetime
from api.fileutils import save_json
import inspect

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
        
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/account/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        
        return jsonResponse
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching market quotes: {e}")
        return None