

# exchange_rate = api.exchange_rates_get_specific_rate('BTC', 'USD')
# print('Time: %s' % exchange_rate['time'])
# print('Base: %s' % exchange_rate['asset_id_base'])
# print('Quote: %s' % exchange_rate['asset_id_quote'])
# print('Rate: %s' % exchange_rate['rate'])
# last_week = datetime.date(2017, 5, 16).isoformat()

# current_rates = api.exchange_rates_get_all_current_rates('BTC')

# print("Asset ID Base: %s" % current_rates['asset_id_base'])
# for rate in current_rates['rates']:
#     print('Time: %s' % rate['time'])
#     print('Quote: %s' % rate['asset_id_quote'])
#     print('Rate: %s' % rate['rate'])

#%%
# Dependencies
import csv
import matplotlib.pyplot as plt
import requests
import pandas as pd
from datetime import datetime
from pprint import pprint
from config import api_key
from config import weather_key


#%%
weather_url = "http://api.openweathermap.org/data/2.5/weather?"
units = "metric"

# Build partial query URL
weather_query_url = f"{weather_url}appid={weather_key}&units={units}&q="

#%%
# # Set the URL to Call for Crypto
# url_base = "https://rest.coinapi.io/v1/"
# url_category = "quotes/"
# symbol_id = "BITSTAMP_SPOT_BTC_USD"
# time_start = "2017-01-01T00:00:00"
# time_end = ""
# limit = "1"
# url_history = url_base + url_category + symbol_id + "/history?time_start=" + time_start + "&timed_end=" + time_end + "&limit=" + limit
# url = url_history

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
cities = ["Paris", "London", "Oslo", "Beijing"]

# set up lists to hold reponse info
lat = []
temp = []

# Loop through the list of cities and perform a request for data on each
for city in cities:
    response = requests.get(weather_query_url + city).json()
    lat.append(response['coord']['lat'])
    temp.append(response['main']['temp'])

print(f"The latitude information received is: {lat}")
print(f"The temperature information received is: {temp}")

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
# create a data frame from cities, lat, and temp
weather_dict = {
    "city": cities,
    "lat": lat,
    "temp": temp
}
weather_data = pd.DataFrame(weather_dict)
weather_data.head()

#%%
# Create Crypto Data Frame
coins_dict = {
    "coins": coins,
    "price_close": close
}

coins_df = pd.DataFrame(coins_dict)
coins_df.head()

# #%%
# # Build a scatter plot for each data type
# plt.scatter(weather_data["lat"], weather_data["temp"], marker="o")

# # Incorporate the other graph properties
# plt.title("Temperature in World Cities")
# plt.ylabel("Temperature (Celsius)")
# plt.xlabel("Latitude")
# plt.grid(True)

# # Save the figure
# plt.savefig("TemperatureInWorldCities.png")

# # Show plot
# plt.show()

#%% Date Stuff
# classmethod datetime.strptime(date_string, format)
# https://docs.python.org/3/library/datetime.html#datetime.datetime.strptime

date = datetime.strptime('Thu, 16 Dec 2010 12:14:05', '%a, %d %b %Y %H:%M:%S')
date.isoformat()




date = datetime.strptime('30 Jul 2015', '%d %b %Y')
date.isoformat()

#%%
item_dict = [
    {
        "item": "bitcoin",
        "date": "2009-01-09T20:00:00",
        "price": 0
},{
        "item": "ethereum",
        "date": "2015-07-30T20:00:00",
        "price": 0
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


#%% Math Attempt

