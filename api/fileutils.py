import json
from loguru import logger
import os
from datetime import datetime

# Save JSON file with folder creation
def save_json(data, file_path = "output.json"):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Write JSON data to the file
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        
        logger.info(f"JSON data successfully saved to {file_path}")
    except Exception as e:
        logger.error(f"Failed to save JSON file: {e}")
