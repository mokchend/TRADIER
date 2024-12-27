import requests
from loguru import logger
from datetime import datetime
from ACCESS_TOKEN import ACCESS_TOKEN

ORDER_API_URL = "https://sandbox.tradier.com/v1/accounts/{account_id}/orders"




def place_multileg_order(account_id):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    
    url = ORDER_API_URL.format(account_id=account_id)
    
    # Multileg order details
    payload = {
        "class": "multileg",
        "type": "credit",  # Limit credit order
        "price": 3.00,  # Limit price
        "duration": "gtc",  # Good 'til Cancelled
    }
    
    # Adding legs
    legs = [
        {"symbol": "SPX250117P06050000", "quantity": 1, "side": "sell_to_open"},
        {"symbol": "SPX250117P06040000", "quantity": 1, "side": "buy_to_open"},
        {"symbol": "SPX250117P05870000", "quantity": 1, "side": "buy_to_open"},
        {"symbol": "SPX250117P05860000", "quantity": 1, "side": "sell_to_open"},
    ]
    
    for i, leg in enumerate(legs):
        payload[f"legs[{i}][symbol]"] = leg["symbol"]
        payload[f"legs[{i}][quantity]"] = leg["quantity"]
        payload[f"legs[{i}][side]"] = leg["side"]
    
    try:
        # Send the POST request
        response = requests.post(url, headers=headers, data=payload)
        
        # Log the request and response
        logger.debug(f"Request Headers: {headers}")
        logger.debug(f"Request Payload: {payload}")
        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Content: {response.text}")
        
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Error placing multileg order: {e}")
        return None


if __name__ == "__main__":
    # Replace with your actual account ID
    account_id = "30312198"
    
    # Place the multileg order
    order_response = place_multileg_order(account_id)
    
    if order_response:
        logger.info("Multileg order placed successfully!")
        print(order_response)
    else:
        logger.error("Failed to place the multileg order.")
