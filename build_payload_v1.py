# Multileg order details
payload = {
    "symbol": "SPX",  # Underlying symbol
    "class": "multileg",
    "type": "credit",  # Limit credit order
    "price": 3.90,  # Limit price
    "duration": "gtc",  # Good 'til Cancelled
}

# Adding legs
legs = [
    {"symbol": "SPX250117P06050000", "quantity": "1", "side": "sell_to_open"},
    {"symbol": "SPX250117P06040000", "quantity": "1", "side": "buy_to_open"},
    {"symbol": "SPX250117P05870000", "quantity": "1", "side": "buy_to_open"},
    {"symbol": "SPX250117P05860000", "quantity": "1", "side": "sell_to_open"},
]

for i, leg in enumerate(legs):
    payload[f"option_symbol[{i}]"] = leg["symbol"]
    payload[f"quantity[{i}]"] = leg["quantity"]
    payload[f"side[{i}]"] = leg["side"]
        
        
print(payload)