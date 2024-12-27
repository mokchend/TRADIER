import requests
from loguru import logger

from ACCESS_TOKEN import ACCESS_TOKEN

OPTIONS_CHAIN_URL = "https://sandbox.tradier.com/v1/markets/options/chains"

def get_option_symbols(symbol, expiration_date):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json",
    }
    params = {
        "symbol": symbol,
        "expiration": expiration_date,
    }

    try:
        # Send GET request to fetch the options chain
        response = requests.get(OPTIONS_CHAIN_URL, headers=headers, params=params)
        logger.debug(f"Request Headers: {headers}")
        logger.debug(f"Request Parameters: {params}")
        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Content: {response.text}")
        response.raise_for_status()
        options_data = response.json()
        return options_data.get("options", {}).get("option", [])
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching options chain: {e}")
        return None

if __name__ == "__main__":
    # Example inputs
    underlying_symbol = "SPX"
    expiration = "2025-01-17"  # Change to desired expiration date

    # Fetch option symbols
    options = get_option_symbols(underlying_symbol, expiration)
    if options:
        logger.info("Options chain retrieved successfully!")
        for option in options:
            print(f"Symbol: {option['symbol']} | Strike: {option['strike']} | Type: {option['option_type']}")
    else:
        logger.error("Failed to retrieve the options chain.")
