def get_multileg_order_params():
   return {    
        'class': 'multileg',
        'symbol': 'SPY',
        'type': 'market',
        'duration': 'day',
        'price': '1.0',
        'option_symbol[0]': 'SPY190605C00282000',
        'side[0]': 'buy_to_open',
        'quantity[0]': '10',
        'option_symbol[1]': 'SPY190605C00286000',
        'side[1]': 'buy_to_close',
        'quantity[1]': '10'
        }
