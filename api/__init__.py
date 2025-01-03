# Mark a Directory as a Python Package:

# It indicates that the directory should be treated as a package, allowing its modules to be imported.
# Initialize the Package:

# It can include package-level variables, imports, or configurations that should be available to all modules in the package.
# Control Imports:

# It can specify what gets imported when the package is imported (using __all__).
# Package-wide Initialization:

# Useful for initializing logging, configuration, or any other package-level setup.

# Example: api/__init__.py
from loguru import logger
from .quotes import get_market_quotes
from .options import get_option_chains
from .orders import place_order, get_orders
from .accounts import get_account_cost_basis, get_account_cost_basis_summary, get_account_positions, get_account_orders, place_equity_order
from .marketdata import get_marketdata_option_chains , get_marketdata_lookup_options_symbols, get_marketdata_quotes
from .mssqlserver import create_connection,  close_connection, execute_query, upsert_account_positions, upsert_account_orders, symbolsToStream
from .fileutils import save_json
from .utils import load_config
from .streamings import create_market_session, get_market_events


logger.info("API package initialized.")

__all__ = [
    "load_config",
    
    "create_market_session",
    "get_market_events"
    
    "create_connection",
    "execute_query",
    "close_connection",
    "upsert_account_positions",
    "upsert_account_orders",
    "symbolsToStream",

    "save_json",
        
    "get_account_orders",
    "get_account_positions",
    "place_equity_order",
    
    "get_marketdata_lookup_options_symbols",
    "get_marketdata_option_chains",
    "get_marketdata_quotes",
    
    
    "get_account_cost_basis_summary",
    "get_account_cost_basis",
    "get_market_quotes",
    "get_option_chains",
    "place_order",
    "get_orders"
]

