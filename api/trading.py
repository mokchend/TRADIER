# Example: api/trading.py
import json
from loguru import logger
import config
import requests
from datetime import datetime
from api.fileutils import save_json
import inspect
from api.order_params import get_multileg_order_params

# https://documentation.tradier.com/brokerage-api/trading/place-equity-order
# https://documentation.tradier.com/brokerage-api/trading/place-equity-order

def place_equity_order_market_day_sell(config, symbol='FTNT', quantity='1.00'):
    return place_equity_order(config, order_type='market', symbol=symbol, quantity=quantity, side='sell', duration='day', price=None, stop=None)

def place_equity_order_market_day_buy(config, symbol='FTNT', quantity='1.00'):
    return place_equity_order(config, order_type='market', symbol=symbol, quantity=quantity, side='buy', duration='day', price=None, stop=None)

def place_equity_order(config, order_type='limit', symbol='FTNT', quantity='10.00', side='buy', duration='gtc', price='1.00', stop=None):
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/orders"
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    function_name = inspect.currentframe().f_code.co_name
        
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    order_data = {
        'class': 'equity',
        'symbol': f'{symbol}',
        'duration': f'{duration}',
        'side': f'{side}',
        'quantity': f'{quantity}',
        'type': f'{order_type}'
    }
    if price:
        order_data['price'] = f'{price}'
    if stop:
        order_data['stop'] = f'{stop}'
    
    try:
        
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/trading/{current_datetime}_{function_name}_request_{symbol}_{side}.json"
        save_json(order_data, fileName)
        logger.debug(f"Order data being sent: {json.dumps(order_data, indent=2)}")

        logger.warning(f"Request URL: {url}")
        logger.warning(f"Headers: {headers}")
        logger.warning(f"Payload: {order_data}")        
        

        response = requests.post(url, headers=headers, data=order_data)
        response.raise_for_status()
        logger.info("Equity order placed successfully.")
        
         
        
        jsonResponse = response.json()
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/trading/{current_datetime}_{function_name}_response_{symbol}_{side}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)
        
        return jsonResponse
    # except requests.exceptions.RequestException as e:
    #     logger.error(f"Error placing equity order: {e}")
    #     return None
    except requests.exceptions.HTTPError as http_err:
        error_details = http_err.response.text
        logger.error(f"Error placing equity order: {error_details}")    
        return None


# https://documentation.tradier.com/brokerage-api/trading/place-multileg-order
def place_a_multileg_order():
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/orders"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    params = get_multileg_order_params()
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        
        
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/trading/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        logger.warning("{function_name} retrieved successfully.")
        
        return jsonResponse
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Cancel an Order: {e}")
        return None

# https://documentation.tradier.com/brokerage-api/trading/cancel-order
def cancel_an_order(order_id):
    
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/orders/{order_id}"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    params = {}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        logger.warning("Cancel an Order retrieved successfully.")
        
        jsonResponse = response.json()
        function_name = inspect.currentframe().f_code.co_name
        current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/account/{current_datetime}_{function_name}.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        
        return jsonResponse
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Cancel an Order: {e}")
        return None