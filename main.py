# Main script: main.py
import json
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


if __name__ == "__main__":
    logger.info("Starting API interactions...")

    # Fetch market quotes for TSLA
    # quotes = get_market_quotes('TSLA')
    # logger.debug(f"Market Quotes: {quotes}")
    # logger.debug(f"Market Quotes: {json.dumps(quotes, indent=4)}")

    # Fetch option chains for TSLA
    # option_chains = get_option_chains('TSLA', '2020-05-22')
    # json pretty print
    # logger.debug(f"Option Chains: {json.dumps(option_chains, indent=4)}")
    # logger.debug(f"Option Chains: {option_chains}")
    
    
    # mktdata_option_chains = get_mktdata_option_chains('SPX', '2025-01-17')
    # filtered_data = [
    #     {
    #         "symbol": option["symbol"],
    #         "strike": option["strike"],
    #         "bid": option["bid"],
    #         "mid": (option["bid"] + option["ask"]) / 2 if option["bid"] is not None and option["ask"] is not None else None,
    #         "ask": option["ask"],                    
    #     }
    #     for option in mktdata_option_chains["options"]["option"]
    # ]
    # logger.debug(f"Option Chains: {json.dumps(filtered_data, indent=4)}")

    # Place an order for TSLA options
    # tesla_call_symbol = 'TSLA200522C00850000'
    # order_response = place_order('TSLA', tesla_call_symbol, 3)
    # logger.debug(f"Order Response: {order_response}")

    # Retrieve all orders
    # all_orders = get_orders()
    # logger.debug(f"Orders: {json.dumps(all_orders, indent=4)}")

    cost_basis = get_account_cost_basis_summary()
    
    # lookup_options_symbols = get_marketdata_lookup_options_symbols('SPX')
    
    
    # Retrieve account positions
    # account_positions = get_account_positions()
    
    # Retrieve account orders
    # account_orders = get_account_orders()

    
    