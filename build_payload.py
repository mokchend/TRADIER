# Main script: main.py
import json
from api.utils import get_standardized_option_symbol
import config
from api import (
    get_market_quotes,
    get_option_chains,
    place_order,
    get_orders,
    get_account_cost_basis,
    get_account_cost_basis_summary,
    get_mktdata_option_chains,
    get_marketdata_lookup_options_symbols,
    get_account_positions,
    get_account_orders,
    save_json
)
from loguru import logger
# Example: api/trading.py
import json
from loguru import logger
import config
import requests
from datetime import datetime
from api.fileutils import save_json
import inspect

def build_payload():
    # Multileg order details
    payload = {
        "symbol": "SPX",  # Underlying symbol
        "class": "multileg",
        "type": "credit",  # Limit credit order
        "price": 5.35,  # Limit price
        "duration": "gtc",  # Good 'til Cancelled
    }

    # Adding legs
    expiration_date = "2025-01-17"
    legs = [
        {"side": "sell_to_open", "quantity": "1", "expiration_date" : expiration_date, "strike_price": 6040, "option_type":"P"},
        {"side": "buy_to_open" , "quantity": "1", "expiration_date" : expiration_date, "strike_price": 6030, "option_type":"P"},
        {"side": "buy_to_open" , "quantity": "1", "expiration_date" : expiration_date, "strike_price": 5890, "option_type":"P"},
        {"side": "sell_to_open", "quantity": "1", "expiration_date" : expiration_date, "strike_price": 5870, "option_type":"P"},
    ]


    # Merge legs into the payload using a loop
    for i, leg in enumerate(legs):
        print(get_standardized_option_symbol(payload["symbol"], leg["expiration_date"], leg["option_type"], leg["strike_price"]))
        payload.update({
            f"option_symbol[{i}]": get_standardized_option_symbol(payload["symbol"], leg["expiration_date"], leg["option_type"], leg["strike_price"]),
            f"quantity[{i}]": leg["quantity"],
            f"side[{i}]": leg["side"]
        })

    return payload



def place_a_multileg_order():
    function_name = inspect.currentframe().f_code.co_name
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    url = f"{config.API_BASE_URL}accounts/{config.ACCOUNT_ID}/orders"
    headers = {
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    }
    params = build_payload()
    fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/trading/{current_datetime}_{function_name}_request.json"
    logger.debug(f"Saving {function_name} to: {fileName}")
    save_json(params, fileName)      
    logger.warning(f"{function_name} retrieved successfully.")
    
    
    try:
        response = requests.post(url, params=params, headers=headers)
        response.raise_for_status()
        
        
        jsonResponse = response.json()
        
        
        fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/trading/{current_datetime}_{function_name}_reponse.json"
        logger.debug(f"Saving {function_name} to: {fileName}")
        save_json(jsonResponse, fileName)      
        logger.warning(f"{function_name} retrieved successfully.")
        
        return jsonResponse
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching Cancel an Order: {e}")
        return None
    
    
place_a_multileg_order()