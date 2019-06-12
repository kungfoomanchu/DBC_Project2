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
#print(ohlcv_hist_url)
#%% 
# Test API Call for Crypto
headers = {'X-CoinAPI-Key' : "040C8FCD-C322-4168-97B8-27E979246DAF"}
response = requests.get(ohlcv_hist_url, headers=headers).json()
#print(response)



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

final_lst = []
row_list = []
dict_final = {}
lst=[]
lst = response


for coin in coins:
    response = requests.get(f'{url_base}{url_ohlcv}{coin}/{asset_id_quote}/history?period_id={period_id}&time_start={time_start}&time_end={time_end}&limit={limit}&include_empty_items={include_empty_items}', headers=headers).json()
    #print("coin is: " + coin)
    for i in range(len(lst)):
        row_list.append(coin)
        row_list.append(lst[i]['time_period_start'])
        row_list.append(lst[i]['price_close'])
        dict_final['coin']=coin

        # str_d0 = lst[i]['time_period_start'][0:10]
        # d1 = datetime.strptime(str_d0, "%Y-%m-%d")
        # d1 = d1.date()
        # dict_final['time_start']=d1
        # dict_final['time_start']=lst[i]['time_period_start']
        dict_final['time_start']=lst[i]['time_period_start'][0:10]
        dict_final['price_close']=lst[i]['price_close']
        final_lst.append(dict_final) 
        dict_final = {} 
# print(final_lst['coin'][0])       
print(final_lst)
# print(len(final_lst))  -- 837
#%%
# print(final_lst[0]['coin']) 
# print(final_lst[0]['time_start']) 
# print(final_lst[0]['price_close']) 

print(final_lst[1]['coin']) 
print(final_lst[1]['time_start']) 
print(final_lst[1]['price_close']) 

# print(len(final_lst)) 
# print(final_lst)
#%%
from flask import (
    Flask,
    render_template,
    jsonify,
    request)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/db.sqlite"

db = SQLAlchemy(app)


#%%
# import necessary libraries

class coinsDB(db.Model):
    __tablename__ = 'coin'

    # id = db.Column(db.Integer, primary_key=False)
    coin_name = db.Column(db.String(64))
    time_start = db.Column(db.String(64))
    price_close = db.Column(db.string(64))

    # def __repr__(self):
    #     return '<Pet %r>' % (self.nickname)


@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()


@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":

        # print(final_lst[0]['coin']) 
        # print(final_lst[0]['time_start']) 
        # print(final_lst[0]['price_close']) 

        for i in range(len(final_lst)):

            coin_name = final_lst[i]['coin']
            time_start = final_lst[i]['time_start']
            price_close = final_lst[i]['price_close']

            rec = coinsDB(coin_name=coin_name, time_start=time_start, price_close=price_close)
            db.session.add(rec)
            db.session.commit()

        return "Thanks for the form data!"

    return render_template("form.html")


@app.route("/api/data")
def list_coins():
    results = db.session.query(coinsDB.coin_name, coinsDB.time_start, coinsDB.price_close).all()

    coin_lst = []
    for result in results:
        coin_lst.append({
            "coin_name": result[0],
            "time_start": result[1],
            "price_close": result[2]
        })
    return jsonify(coin_lst)


@app.route("/")
def home():
    return "Welcome!"


if __name__ == "__main__":
    app.run()


#%%
