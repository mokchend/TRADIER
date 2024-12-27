# Example: api/quotes.py
import json
from loguru import logger
import config
import requests

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
        # return {json.dumps(response.json(), indent=4)}
        return response.json()
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
        'start': 'yyyy-mm-dd',
        'end': 'yyyy-mm-dd',
        'symbol': symbol
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        logger.info("Get an account’s cost basis retrieved successfully.")
        return response.json()
        # return {json.dumps(response.json(), indent=4)}
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching an account’s cost basis: {e}")
        return None