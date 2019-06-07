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
from datetime import date
from datetime import datetime
import numpy as np

#from config import api_key
#from config import weather_key


#%%
# OHLCV Historical URL
url_base = "https://rest.coinapi.io/v1/"
url_ohlcv = "ohlcv/"
asset_id_base = "BTC"
asset_id_quote = "USD"
period_id = "1DAY"
time_start = "2017-01-01T00:00:00"
time_end = "2017-02-01T00:00:00"
#time_end = ""
limit = "100" #cann be max of 100000
include_empty_items = False
ohlcv_hist_url = f'{url_base}{url_ohlcv}{asset_id_base}/{asset_id_quote}/history?period_id={period_id}&time_start={time_start}&time_end={time_end}&limit={limit}&include_empty_items={include_empty_items}'

#%% 
# Test API Call for Crypto
headers = {'X-CoinAPI-Key' : "B5D6CFCB-2E3F-4318-AF5B-6D777D0A69EC"}
response = requests.get(ohlcv_hist_url, headers=headers).json()




#%%

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
str_d0 = time_start[0:10]
str_d1 = time_end[0:10]


d1 = datetime.strptime(str_d0, "%Y-%m-%d")
d2 = datetime.strptime(str_d1, "%Y-%m-%d")

d1 = d1.date()
d2 = d2.date()


delta  = d2 - d1
days  = delta.days

coins = ["BTC", "ETH"]

# Set up lists to hold response info
close = []

# Loop
for coin in coins:
    response = requests.get(f'{url_base}{url_ohlcv}{coin}/{asset_id_quote}/history?period_id={period_id}&time_start={time_start}&time_end={time_end}&limit={limit}&include_empty_items={include_empty_items}', headers=headers).json()
    close.append(response[0]['price_close'])





# for i in range(days):
#     print(i)
#%%
# Create Crypto Data Frame
coins_dict = {
    "coins": coins,
    "price_close": close
}

coins_df = pd.DataFrame(coins_dict)
coins_df.head()




#%%



str_d0 = time_start[0:10]
str_d1 = time_end[0:10]


d1 = datetime.strptime(str_d0, "%Y-%m-%d")
d2 = datetime.strptime(str_d1, "%Y-%m-%d")

d1 = d1.date()
d2 = d2.date()


delta  = d2 - d1
days  = delta.days
#print(days)

# for i in range(days):
#     print(i)


dict_final = {}



lst = response


for coin in coins:
    response = requests.get(f'{url_base}{url_ohlcv}{coin}/{asset_id_quote}/history?period_id={period_id}&time_start={time_start}&time_end={time_end}&limit={limit}&include_empty_items={include_empty_items}', headers=headers).json()
    final_lst = []

    for i in range(len(lst)):
        final_lst.append(coin)
        final_lst.append(lst[i]['time_period_start'])
        final_lst.append(lst[i]['price_close'])
    dict_final[coin] = final_lst    
print(dict_final)       



#%%
print(dict_final) 

#%%
