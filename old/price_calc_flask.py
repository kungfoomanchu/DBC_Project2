item_dict = [
    {
        "item": "bitcoin",
        "date": "2009-01-09T20:00:00",
        "price": 0
},{
        "item": "bitcoin_max",
        "date": "2017-12-17T20:00:00",
        "price": 19783.06
},{
        "item": "ethereum",
        "date": "2015-07-30T20:00:00",
        "price": 0
},{
        "item": "ethereum_max",
        "date": "2018-01-13T20:00:00",
        "price": 1432.88
},{
        "item": "ps4",
        "date": "2013-11-15T20:00:00",
        "price": 399
},{
        "item": "pizza",
        "date": "2010-05-22T20:00:00",
        "price": 30/10000
},{
        "item": "MacBook Pro 2012",
        "date": "2012-07-30T20:00:00",
        "price": 1199
},{
        "item": "Oculus Rift",
        "date": "2016-03-28T20:00:00",
        "price": 599
}]


#%%
# Dependencies
import csv
import matplotlib.pyplot as plt
import requests
import pandas as pd
from pprint import pprint
from config import api_key


#%%
# OHLCV Historical URL
url_base = "https://rest.coinapi.io/v1/"
url_ohlcv = "ohlcv/"
asset_id_base = "BTC"
asset_id_quote = "USD"
period_id = "1DAY"
time_start = "2017-01-01T00:00:00"
time_end = "2017-02-01T00:00:00"
limit = "100" #cann be max of 100000
include_empty_items = False
ohlcv_hist_url = f'{url_base}{url_ohlcv}{asset_id_base}/{asset_id_quote}/history?period_id={period_id}&time_start={time_start}&time_end={time_end}&limit={limit}&include_empty_items={include_empty_items}'

#%%
# Test API Call for Crypto
headers = {'X-CoinAPI-Key' : api_key}
response = requests.get(ohlcv_hist_url, headers=headers).json()

pprint(response)


#%%
# Crypto Multiple Coins
coins = ["BTC", "ETH"]

# Set up lists to hold response info
close = []

# Loop
for coin in coins:
    response = requests.get(f'{url_base}{url_ohlcv}{coin}/{asset_id_quote}/history?period_id={period_id}&time_start={time_start}&time_end={time_end}&limit={limit}&include_empty_items={include_empty_items}', headers=headers).json()
    close.append(response)

print(f"The close prices for BTC then ETH: {close}")


#%%
# Create Crypto Data Frame
coins_dict = {
    "coins": coins,
    "price_close": close
}

coins_df = pd.DataFrame(coins_dict)
coins_df.head()


#%%
