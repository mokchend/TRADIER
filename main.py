# Main script: main.py
from api import get_market_quotes, get_option_chains, place_order, get_orders
from loguru import logger

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
