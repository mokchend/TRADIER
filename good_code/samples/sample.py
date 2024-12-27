import requests
from loguru import logger

# Tradier Sandbox API endpoint and token
PROFILE_API_URL = "https://sandbox.tradier.com/v1/user/profile"
POSITIONS_API_URL = "https://sandbox.tradier.com/v1/accounts/{{account_id}}/positions"
ACCESS_TOKEN = "Wu0KkJAmAJNobU5JANDoelN8993W"  # Replace with your sandbox access token

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

if __name__ == "__main__":
    account_info = get_account_details()
    if account_info:
        logger.info("Sandbox account details retrieved successfully.")
        print(account_info)

        # Extract account ID and fetch positions
        account_id = account_info.get("profile", {}).get("account", {}).get("account_number")
        if account_id:
            positions = get_open_positions(account_id)
            if positions:
                logger.info("Open positions retrieved successfully.")
                print(positions)
            else:
                logger.error("Failed to retrieve open positions.")
        else:
            logger.error("Account ID not found in profile data.")
    else:
        logger.error("Failed to retrieve sandbox account details.")
