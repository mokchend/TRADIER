import requests
from loguru import logger

# Replace with your Tradier API token


import json
# Load account ID from config file
with open('sandbox.json', 'r') as config_file:
    config = json.load(config_file)
    account_id = config["account_id"]
    ACCESS_TOKEN = config["ACCESS_TOKEN"]

BASE_URL = "https://api.tradier.com/v1/markets/quotes"


def get_option_prices(option_symbol):
    """
    Retrieve Bid, Ask, and Mid prices for a given option symbol.

    Parameters:
        option_symbol (str): The symbol of the option to retrieve prices for.

    Returns:
        dict: A dictionary containing the Bid, Ask, and Mid prices.
    """
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Accept": "application/json",
    }

    params = {
        "symbols": option_symbol,
    }

    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        
        data = response.json()
        quote = data.get("quotes", {}).get("quote", {})

        # Extract Bid, Ask, and calculate Mid price
        bid = quote.get("bid")
        ask = quote.get("ask")
        
        if bid is not None and ask is not None:
            mid = (bid + ask) / 2
        else:
            mid = None

        return {
            "Bid": bid,
            "Ask": ask,
            "Mid": mid,
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching option prices: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    option_symbol = "SPXW250117P09000000"  # Replace with your option symbol
    prices = get_option_prices(option_symbol)

    if prices:
        print(f"Prices for {option_symbol}:")
        print(f"Bid: {prices['Bid']}")
        print(f"Ask: {prices['Ask']}")
        print(f"Mid: {prices['Mid']}")
    else:
        print("Failed to retrieve option prices.")
