# Version 3.6.1    
import json
from loguru import logger
from api.mssqlserver import upsert_account_orders, upsert_account_positions, upsert_account_orders
import requests

from datetime import datetime
from api.fileutils import save_json
import inspect

# https://documentation.tradier.com/brokerage-api/streaming/get-markets-events
# {
#     'type': 'trade', 
#     'symbol': 'MSTR', 
#     'exch': 'Q', 
#     'price': '289.62', 
#     'size': '1184593', 
#     'cvol': '1144373', 
#     'date': '1735678800174', 
#     'last': '289.62'
# }
def get_market_events(config):
    headers = {
        'Accept': 'application/json'
    }

    payload = { 
        'sessionid': f'{create_market_session(config)}',
        'symbols': 'FTNT,CRM,MSTR',
        'linebreak': True
    }

    r = requests.get('https://stream.tradier.com/v1/markets/events', stream=True, params=payload, headers=headers)
    for line in r.iter_lines():
        if line:
            # print(json.loads(line))
            # logger.info(line)
            # Example byte string
            byte_data = line
            # Decode to string
            decoded_string = byte_data.decode('utf-8')
            # Parse as JSON
            parsed_data = json.loads(decoded_string)
            logger.warning(f"{parsed_data}")


def create_market_session(config):
    url = f"{config.API_BASE_URL}markets/events/session"
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    function_name = inspect.currentframe().f_code.co_name
    data={};
    headers={
        'Authorization': f'Bearer {config.ACCESS_TOKEN}', 
        'Accept': 'application/json'
    };
    
    response = requests.post(f'{url}',
        data=data,
        headers=headers
    )
    

    json_response = response.json()
    # print(response.status_code)
    # print(json_response)
    logger.warning(f"Stream response: {json_response}")
    
    fileName = f"{config.ROOT_FOLDER}/datas/tradier_accounts/{config.ACCOUNT_ID}/markets/{current_datetime}_{function_name}_response.json"
    save_json(json_response, fileName)
    logger.warning(f"Stream output: {json.dumps(json_response, indent=2)}")
    
    if response.status_code == 200:
        json_response = response.json()
        # print(json_response)  # Debugging: Ensure response structure is as expected
        return json_response['stream']['sessionid']
    else:
        logger.error(f"Failed to create market session: {response.status_code} {response.text}")
        raise Exception("Market session creation failed")

