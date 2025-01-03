# Main script: main.py
import json
from api.trading import place_equity_order_market_day_buy, place_equity_order_market_day_sell
import config
from api import (
    get_market_quotes,
    get_option_chains,
    place_order,
    get_orders,
    get_account_cost_basis,
    get_account_cost_basis_summary,
    get_marketdata_option_chains,
    get_marketdata_lookup_options_symbols,
    get_account_positions,
    get_account_orders,
    get_marketdata_quotes,
    save_json, 
    place_equity_order,
    load_config,
    create_market_session,
    get_market_events
)

from loguru import logger


if __name__ == "__main__":
    logger.info("Starting API interactions...")
    # Define the environment: 'sandbox', 'production1', 'production2'
    environment = "production1"  # Change this based on your test

    # Load configuration
    config = load_config(environment)

    
    # quotes = get_market_quotes('TSLA')
    
    # option_chains = get_option_chains('TSLA', '2025-01-17')
    
    
    # mktdata_option_chains = get_mktdata_option_chains('SPX', '2025-01-17')

    # tesla_call_symbol = 'TSLA200522C00850000'
    # order_response = place_order('TSLA', tesla_call_symbol, 3)
    
    # all_orders = get_orders()

    
    
    # lookup_options_symbols = get_marketdata_lookup_options_symbols('SPX')
    
    # get_account_cost_basis("CRM")
    
    # cost_basis = get_account_cost_basis_summary() # Bug Tradier: always return null
    # account_positions = get_account_positions()
    
    # account_orders = get_account_orders()
    
    

    # marketdata_quotes = get_marketdata_quotes('CRM,MSTR')
    
    # place_equity_order(config, order_type='limit', symbol='CRM', quantity='10.00', side='buy', duration='gtc', price='93.5', stop=None)
    # create_market_session(config)
    # get_market_events(config)
    place_equity_order_market_day_buy(config, symbol='TSLA', quantity='1')
    place_equity_order_market_day_sell(config, symbol='TSLA', quantity='1')