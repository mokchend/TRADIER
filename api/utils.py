import json
from loguru import logger
import os
from datetime import datetime

def get_standardized_option_symbol(symbol, expiration_date, option_type, strike_price):
    """
    Generate the standardized options contract symbol.
    
    :param symbol: The underlying symbol (e.g., SPX)
    :param expiration_date: Expiration date in 'YYYY-MM-DD' format (e.g., '2025-01-17')
    :param option_type: Option type, 'C' for Call or 'P' for Put
    :param strike_price: Strike price as a float (e.g., 6050.00)
    :return: Standardized options contract symbol (e.g., SPX250117P06050000)
    """
    try:
        # Ensure the strike price is a valid float and format it
        strike_price = float(strike_price)  # Ensure it's a float
        strike_price_str = f"{int(strike_price * 1000):08d}"  # Convert to an 8-digit integer

        # Convert expiration date to YYMMDD format
        expiration_str = expiration_date[2:].replace("-", "")
        
        # Combine all parts into the standardized symbol
        standardized_symbol = f"{symbol}{expiration_str}{option_type}{strike_price_str}"
        return standardized_symbol
    
    except ValueError as e:
        raise ValueError(f"Invalid input: {e}")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")
