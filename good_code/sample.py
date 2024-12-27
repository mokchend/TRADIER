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

def place_order(symbol, option_symbol, quantity):
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/orders"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    data = {
        'class': 'option', 
        'symbol': symbol, 
        'option_symbol': option_symbol, 
        'side': 'buy_to_open', 
        'quantity': str(quantity), 
        'type': 'market', 
        'duration': 'day'
    }
    try:
        response = requests.post(url, data=data, headers=headers)
        response.raise_for_status()
        logger.info("Order placed successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error placing order: {e}")
        return None

def get_orders():
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/orders"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        logger.info("Orders retrieved successfully.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching orders: {e}")
        return None

if __name__ == "__main__":
    logger.info("Starting API interactions...")

    # Fetch market quotes for TSLA
    quotes = get_market_quotes('TSLA')
    logger.debug(f"Market Quotes: {quotes}")

    # Fetch option chains for TSLA
    option_chains = get_option_chains('TSLA', '2020-05-22')
    logger.debug(f"Option Chains: {option_chains}")

    # Place an order for TSLA options
    tesla_call_symbol = 'TSLA200522C00850000'
    order_response = place_order('TSLA', tesla_call_symbol, 3)
    logger.debug(f"Order Response: {order_response}")

    # Retrieve all orders
    all_orders = get_orders()
    logger.debug(f"Orders: {all_orders}")
