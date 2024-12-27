import requests
from loguru import logger
from datetime import datetime, timedelta

from ACCESS_TOKEN import ACCESS_TOKEN

# Tradier Sandbox API endpoint and token
PROFILE_API_URL = "https://sandbox.tradier.com/v1/user/profile"
POSITIONS_API_URL = "https://sandbox.tradier.com/v1/accounts/{{account_id}}/positions"
ORDER_API_URL = "https://sandbox.tradier.com/v1/accounts/{{account_id}}/orders"

# Function to get account details from the Sandbox
def get_account_details():
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json",
    }

    try:
        response = requests.get(PROFILE_API_URL, headers=headers)
        logger.debug(f"Request Headers: {headers}")
        logger.debug(f"Response Content: {response.text}")
        response.raise_for_status()
        account_data = response.json()
        return account_data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching account details: {e}")
        return None

# Function to get open positions from the Sandbox
def get_open_positions(account_id):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json",
    }
    url = POSITIONS_API_URL.replace("{{account_id}}", account_id)

    try:
        response = requests.get(url, headers=headers)
        logger.debug(f"Request Headers: {headers}")
        logger.debug(f"Response Content: {response.text}")
        response.raise_for_status()
        positions_data = response.json()
        return positions_data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching open positions: {e}")
        return None

# Function to place a multi-leg combo options order

def place_combo_order(account_id, legs, order_type, price, duration="gtc"):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    url = ORDER_API_URL.replace("{{account_id}}", account_id)

    # Generate payload
    payload = {
        "class": "multileg",
        "type": order_type,
        "price": price,
        "duration": duration,
        "expire": "2024-01-17",  # Ensure valid future date
    }

    if len(legs) < 2:
        logger.error("Invalid number of legs. At least two legs are required for a multileg order.")
        return None

    for i, leg in enumerate(legs):
        payload[f"legs[{i}][symbol]"] = leg["symbol"]
        payload[f"legs[{i}][quantity]"] = leg["quantity"]
        payload[f"legs[{i}][side]"] = leg["side"]

    try:
        response = requests.post(url, headers=headers, data=payload)
        logger.debug(f"Request Headers: {headers}")
        logger.debug(f"Request Payload: {payload}")
        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Content: {response.text}")
        response.raise_for_status()
        order_data = response.json()
        return order_data
    except requests.exceptions.RequestException as e:
        logger.error(f"Error placing combo order: {e}")
        return None


if __name__ == "__main__":
    account_info = get_account_details()
    if account_info:
        logger.info("Sandbox account details retrieved successfully.")
        print(account_info)

        # Extract account ID
        account_id = account_info.get("profile", {}).get("account", {}).get("account_number")
        if account_id:
            # Define multi-leg trade details based on your screenshot
            legs = [
                {"symbol": "SPX   240117P06050", "quantity": 1, "side": "sell_to_open"},
                {"symbol": "SPX   240117P06040", "quantity": 1, "side": "buy_to_open"},
                {"symbol": "SPX   240117P05870", "quantity": 1, "side": "buy_to_open"},
                {"symbol": "SPX   240117P05860", "quantity": 1, "side": "sell_to_open"},
            ]
            order_type = "limit"
            price = 3.00  # Limit price

            # Place the combo order
            order_response = place_combo_order(account_id, legs, order_type, price)
            if order_response:
                logger.info("Combo order placed successfully.")
                print(order_response)
            else:
                logger.error("Failed to place the combo order.")
        else:
            logger.error("Account ID not found in profile data.")
    else:
        logger.error("Failed to retrieve sandbox account details.")
