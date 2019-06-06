'''
Bitcoin 9 January 2009
Ethereum    30 July 2015
PS4 November 15, 2013   $399
Bitcoin Pizza May 22, 2010, a programmer purchased two large Papa John’s pizzas for 10,000 bitcoins, worth about $30 at the time

MacBook Pro 13-inch, mid-2012
Type  Midsize
Screen size  13.322
Screen resolution  1280 x 800
Bundled OS  Mac OS
CPU family  Core i5
Processor speed  2.519
System RAM  41
Pointing device  Trackpad
Video outputs  DisplayPort
Maximum battery life  Up to 720
From $1199.00

Oculus Rift March 28, 2016  $599.99

'''

#%%
# Dependencies
import csv
import matplotlib.pyplot as plt
import requests
import pandas as pd
from pprint import pprint
from config import api_key
from config import weather_key


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
    close.append(response[0]['price_close'])

print(f"The close prices for BTC then ETH: {close}")


#%%
# Create Crypto Data Frame
coins_dict = {
    "coins": coins,
    "price_close": close
}

coins_df = pd.DataFrame(coins_dict)
coins_df.head()
