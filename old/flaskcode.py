import csv
# import matplotlib.pyplot as plt
import requests
import pandas as pd
from pprint import pprint
from datetime import date, datetime
import numpy as np

from config import api_key


import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect


from flask import (
    Flask,
    render_template,
    jsonify,
    request)

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/db.sqlite"

db = SQLAlchemy(app)


# class itemsDB(db.Model):
#     __tablename__ = 'items' 
#     __table_args__ = {'extend_existing': True}

#     id = db.Column(db.Integer, primary_key=True)
#     item = db.Column(db.String(64))
#     name = db.Column(db.String(64))
#     date = db.Column(db.String(64))
#     price = db.Column(db.String(64))


#     def __repr__(self):
#         return '<itemsDB %r>' % (self.item)

# @app.before_first_request
# def setup():
#     # Recreate database each time for demo
#     # db.drop_all()
#     # db.create_all()

@app.route("/items")
def list_items():
    # if request.method == "POST":
    item_dict = [
    {
        "item": "bitcoin",
        "name": "Bitcoin",
        "date": "2009-01-09T20:00:00",
        "price": 0
    },{
            "item": "bitcoin_max",
            "name": "Bitcoin Peak",
            "date": "2017-12-17T20:00:00",
            "price": 19783.06
    },{
            "item": "ethereum",
            "name": "Ethereum",
            "date": "2015-07-30T20:00:00",
            "price": 0
    },{
            "item": "ethereum_max",
            "name": "Ethereum Peak",
            "date": "2018-01-13T20:00:00",
            "price": 1432.88
    },{
            "item": "ps4",
            "name": "PS4",
            "date": "2013-11-15T20:00:00",
            "price": 399
    },{
            "item": "pizza",
            "name": "Bitcoin Pizza",
            "date": "2010-05-22T20:00:00",
            "price": 30
    },{
            "item": "macbook",
            "name": "MacBook Pro 2012",
            "date": "2012-07-30T20:00:00",
            "price": 1199
    },{
            "item": "oculus",
            "name": "Oculus Rift",
            "date": "2016-03-28T20:00:00",
            "price": 599
    },{
            "item": "fiftycent",
            "name": "50 Cent",
            "date": "2014-02-11T20:00:00",
            "price": 400000
    }]

    item_df = pd.DataFrame(item_dict)
    # item_df = item_df.set_index("item")
    item_df
    # print(item_df)


    from sqlalchemy import create_engine
    engine = create_engine('sqlite://', echo=False)
    # engine = create_engine("sqlite:///../database.sqlite")

    item_df.to_sql('items_tbl', con=engine)
    # engine.execute("SELECT * FROM items_tbl").fetchall()




    # engine = create_engine('sqlite://', echo=False)
    results = engine.execute("SELECT * FROM items_tbl").fetchall()
    lst_data1 = []


    # pets = []
    for result in results:
        lst_data1.append({
            "date": result[1],
            "item": result[2],
            "name": result[3],
            "price": result[4]


        })
    return jsonify(lst_data1)



@app.route("/coin")
def list_coins():

    url_base = "https://rest.coinapi.io/v1/"
    url_ohlcv = "ohlcv/"
    asset_id_base = "BTC"
    asset_id_quote = "USD"
    period_id = "1DAY"
    time_start = "2017-01-01T00:00:00"
    time_end = "2017-01-05T00:00:00"
    #time_end = ""
    limit = "100" #cann be max of 100000
    include_empty_items = False
    ohlcv_hist_url = f'{url_base}{url_ohlcv}{asset_id_base}/{asset_id_quote}/history?period_id={period_id}&time_start={time_start}&time_end={time_end}&limit={limit}&include_empty_items={include_empty_items}'

    # Test API Call for Crypto
    headers = {'X-CoinAPI-Key' : api_key}
    response = requests.get(ohlcv_hist_url, headers=headers).json()

    # Crypto Multiple Coins
    coins = ["BTC"]

    # Set up lists to hold response info
    close = []

    final_lst = []
    row_list = []
    dict_final = {}
    lst=[]
    lst = response


    for coin in coins:
        response = requests.get(f'{url_base}{url_ohlcv}{coin}/{asset_id_quote}/history?period_id={period_id}&time_start={time_start}&time_end={time_end}&limit={limit}&include_empty_items={include_empty_items}', headers=headers).json()
        for i in range(len(lst)):
            row_list.append(coin)
            row_list.append(lst[i]['time_period_start'])
            row_list.append(lst[i]['price_close'])
            dict_final['coin']=coin

            dict_final['time_start']=lst[i]['time_period_start'][0:10]
            dict_final['price_close']=lst[i]['price_close']
            final_lst.append(dict_final) 
            dict_final = {} 

    print(final_lst)
    coins_df = pd.DataFrame(final_lst)

    from sqlalchemy import create_engine
    engine = create_engine('sqlite://', echo=False)

    # engine = create_engine("sqlite:///../database.sqlite")

    coins_df.to_sql('coins_tbl', con=engine)


    results = engine.execute("SELECT * FROM coins_tbl").fetchall()
    lst_data1 = []

    for result in results:
        lst_data1.append({
            "coin": result[1],
            "price_close": result[2],
            "time_period_start": result[3]


        })
    return jsonify(lst_data1)


@app.route("/quantity/<item>")
def get_quantity(item):
    item_dict = [
    {
        "item": "bitcoin",
        "name": "Bitcoin",
        "date": "2009-01-09T20:00:00",
        "price": 0
    },{
            "item": "bitcoin_max",
            "name": "Bitcoin Peak",
            "date": "2017-12-17T20:00:00",
            "price": 19783.06
    },{
            "item": "ethereum",
            "name": "Ethereum",
            "date": "2015-07-30T20:00:00",
            "price": 0
    },{
            "item": "ethereum_max",
            "name": "Ethereum Peak",
            "date": "2018-01-13T20:00:00",
            "price": 1432.88
    },{
            "item": "ps4",
            "name": "PS4",
            "date": "2013-11-15T20:00:00",
            "price": 399
    },{
            "item": "pizza",
            "name": "Bitcoin Pizza",
            "date": "2010-05-22T20:00:00",
            "price": 30
    },{
            "item": "macbook",
            "name": "MacBook Pro 2012",
            "date": "2012-07-30T20:00:00",
            "price": 1199
    },{
            "item": "oculus",
            "name": "Oculus Rift",
            "date": "2016-03-28T20:00:00",
            "price": 599
    },{
            "item": "fiftycent",
            "name": "50 Cent",
            "date": "2014-02-11T20:00:00",
            "price": 400000
    }]

    item_df = pd.DataFrame(item_dict)
    item_df = item_df.set_index("item")
    print(item)


    item_date = item_df.loc[item]["date"]
    item_price = item_df.loc[item]["price"]
    item_name = item_df.loc[item]["name"]

    print(item_date)
    print(item_price)


    # URL Variables
    time_start = item_date
    url_base = "https://rest.coinapi.io/v1/"
    url_ohlcv = "ohlcv/"
    asset_id_base = "BTC"
    asset_id_quote = "USD"
    period_id = "1DAY"
    include_empty_items = False

    # URL Construction
    ohlcv_hist_url = f'{url_base}{url_ohlcv}{asset_id_base}/{asset_id_quote}/history?period_id={period_id}&time_start={time_start}&limit=1&include_empty_items={include_empty_items}'

    # API Call for Crypto
    headers = {'X-CoinAPI-Key' : api_key}
    response = requests.get(ohlcv_hist_url, headers=headers).json()
    pprint(response)
    bitcoin_value_on_item_day = response[0]['price_close']
    # print(bitcoin_value_on_item_day)

    # Quantity of Bitcoin for Price of Item
    bitcoin_shares = item_price / bitcoin_value_on_item_day
    # print(bitcoin_shares)

    # ==========
    # Item Quantity at Max Bitcoin
    item_quantity_max = ((item_df.loc["bitcoin_max"]["price"])*bitcoin_shares)/item_price
    # print(item_quantity_max)

    # ==========
    # Item Quantity Today
    today = datetime.datetime.now() - datetime.timedelta(hours = 8)
    today = today.isoformat()

    time_start = today[:19]
    ohlcv_hist_url = f'{url_base}{url_ohlcv}{asset_id_base}/{asset_id_quote}/history?period_id={period_id}&time_start={time_start}&limit=1&include_empty_items={include_empty_items}'

    headers = {'X-CoinAPI-Key' : api_key}
    response = requests.get(ohlcv_hist_url, headers=headers).json()

    bitcoin_today = response[0]['price_close']

    item_quantity_current = (bitcoin_today*bitcoin_shares)/item_price
    # print(item_quantity_current)

    return f'You would have {item_quantity_max} {item_name}s if you sold at the peak. You would have {item_quantity_current} {item_name}s if you sold at the peak.'






if __name__ == "__main__":
    app.run()