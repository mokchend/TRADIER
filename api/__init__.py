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


logger.info("API package initialized.")

__all__ = ["get_market_quotes", "get_option_chains", "place_order", "get_orders"]

