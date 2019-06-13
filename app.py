# For Flask
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

# For Database
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import (
        create_engine,
        inspect,
        func)
from flask_sqlalchemy import SQLAlchemy

# from flask_pymongo import PyMongo

# For ItemQuantity
import requests
import pandas as pd
import datetime
import pprint as pprint
import json
import os

# User Files
# import price_calc_flask
from config import api_key

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/db.sqlite"

db = SQLAlchemy(app)

# class Coin(db.Model):
#     __tablename__ = 'coins'

#     id = db.Column(db.Integer, primary_key=True)
#     coinName = db.Column(db.String(64))
#     date = db.Column(db.String)
#     price_close = db.Column(db.Integer)

#     def __repr__(self):
#         return '<Coin %r>' % (self.name)


#################################################
# Flask Before First Request
#################################################
# Before first request
# @app.before_first_request
# def setup():
#     # Recreate database each time for demo
#     db.drop_all()
#     db.create_all()



#################################################
# Flask Index
#################################################
# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

#################################################
# Line Chart
#################################################
# create route that renders index.html template
@app.route("/line")
def line():
    return render_template("index3.html")

#################################################
# Relative Size
#################################################
# create route that renders index.html template
@app.route("/circles")
def circles():
    return render_template("circles.html")

#################################################
# Flask Items Route
#################################################
@app.route("/items")
def list_items():
    item_dict = [
    {
        "item": "bitcoin",
        "name": "Bitcoin",
        "date": "2009-01-09T20:00:00",
        "price": 0,
        "svg": "static/images/bitcoin.svg",
        "bitcoin_price": 0
    },{
        "item": "bitcoin_max",
        "name": "Bitcoin Peak",
        "date": "2017-12-17T20:00:00",
        "price": 19783.06,
        "svg": "static/images/bitcoin.svg",
        "bitcoin_price": 19783.06
    },{
        "item": "ps4",
        "name": "PS4",
        "date": "2013-11-15T20:00:00",
        "price": 399,
        "svg": "static/images/playstation-logo.svg",
        "bitcoin_price": 412.0
    },{
        "item": "pizza",
        "name": "Bitcoin Pizza",
        "date": "2010-05-22T20:00:00",
        "price": 30,
        "svg": "static/images/pizza-svgrepo-com-simple.svg",
        "bitcoin_price": 0.003
    },{
        "item": "macbook",
        "name": "MacBook Pro 2012",
        "date": "2012-07-30T20:00:00",
        "price": 1199,
        "svg": "static/images/laptop.svg",
        "bitcoin_price": 9.0979
    },{
        "item": "oculus",
        "name": "Oculus Rift",
        "date": "2016-03-28T20:00:00",
        "price": 599,
        "svg": "static/images/oculus-rift-virtual-reality-svgrepo-com.svg",
        "bitcoin_price": 419.995
    },{
        "item": "fiftycent",
        "name": "50 Cent",
        "date": "2014-02-11T20:00:00",
        "price": 400000,
        "svg": "static/images/50cent-cd.svg",
        "bitcoin_price": 664.666
    },{
        "item": "cigs",
        "name": "365 Packs of Cigarettes in 2014",
        "date": "2014-12-31T20:00:00",
        "price": 1989.25,
        "svg": "static/images/cigarette-box-lighter.svg",
        "bitcoin_price": 317.0
    }]

    item_df = pd.DataFrame(item_dict)
    #item_df = item_df.set_index("item")
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

    for result in results:
        lst_data1.append({
            "date": result[2],
            "item": result[3],
            "name": result[4],
            "price": result[5],
            "svg": result[6],
            "bitcoin_price": result[1]
        })
    return jsonify(lst_data1)



#################################################
# Flask Coin API Route
#################################################
@app.route("/coin")
def list_coins():
    url_base = "https://rest.coinapi.io/v1/"
    url_ohlcv = "ohlcv/"
    asset_id_base = "BTC"
    asset_id_quote = "USD"
    period_id = "1DAY"
    time_start = "2010-02-01T00:00:00"
    # today = datetime.datetime.now() - datetime.timedelta(hours = 8)
    # today = today.isoformat()
    # time_end = today
    time_end = ""
    limit = "100000" #cann be max of 100000
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
    # lst = response

    print(time_start)
    print(time_end)

    for coin in coins:
        response = requests.get(f'{url_base}{url_ohlcv}{coin}/{asset_id_quote}/history?period_id={period_id}&time_start={time_start}&time_end={time_end}&limit={limit}&include_empty_items={include_empty_items}', headers=headers).json()
        lst = response
        print(lst)
        for i in range(len(lst)):
            # row_list.append(coin)
            # row_list.append(lst[i]['time_period_start'])
            # row_list.append(lst[i]['price_close'])
            dict_final['coin']=coin

            dict_final['time_start']=lst[i]['time_period_start'][0:10]
            dict_final['price_close']=lst[i]['price_close']
            final_lst.append(dict_final)
            dict_final = {}

    # print(final_lst)
    coins_df = pd.DataFrame(final_lst)
    print(coins_df)
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///database/coin_db.sqlite', echo=False)
    
    # engine = create_engine('sqlite://', echo=False)
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



#################################################
# Save the Database
#################################################

@app.route("/sqlite")
def sql_detail():

   from sqlalchemy import create_engine

   engine = create_engine('sqlite:///database/coin_db.sqlite', echo=False)

   results = engine.execute("SELECT * FROM coins_tbl").fetchall()
   lst_data1 = []

   for result in results:
       lst_data1.append({
           "coin": result[1],
           "price_close": result[2],
           "time_period_start": result[3]
       })
   print (lst_data1)
   with open('temp/coin.json', 'a+') as f:
       json.dump(lst_data1, f)

   return jsonify(lst_data1)

#################################################
# End Save the Database
#################################################



#################################################
# Flask Last part of Setup
#################################################
@app.route("/quantity_json/<item>")

def get_quantity_json(item):
    #############################################
    # Internal Item Call
    #############################################
    url_internal = "http://localhost:5000/items"
    response_internal = requests.get(url_internal).json()
    response_internal = json.dumps(response_internal)
    # The above line gives the output {items_route} below
    # items_route = [{"date": "2009-01-09T20:00:00", "item": "bitcoin", "name": "Bitcoin", "price": 0.0}, {"date": "2017-12-17T20:00:00", "item": "bitcoin_max", "name": "Bitcoin Peak", "price": 19783.06}, {"date": "2015-07-30T20:00:00", "item": "ethereum", "name": "Ethereum", "price": 0.0}, {"date": "2018-01-13T20:00:00", "item": "ethereum_max", "name": "Ethereum Peak", "price": 1432.88}, {"date": "2013-11-15T20:00:00", "item": "ps4", "name": "PS4", "price": 399.0}, {"date": "2010-05-22T20:00:00", "item": "pizza", "name": "Bitcoin Pizza", "price": 30.0}, {"date": "2012-07-30T20:00:00", "item": "macbook", "name": "MacBook Pro 2012", "price": 1199.0}, {"date": "2016-03-28T20:00:00", "item": "oculus", "name": "Oculus Rift", "price": 599.0}, {"date": "2014-02-11T20:00:00", "item": "fiftycent", "name": "50 Cent", "price": 400000.0}, {"date": "2014-02-11T20:00:00", "item": "cigs", "name": "365 Packs of Cigarettes in 2014", "price": 1989.25}]
    response_internal = json.loads(response_internal)
    data = response_internal
    df = pd.DataFrame.from_dict(data, orient='columns')
    #pprint(df)

    #item_df = pd.DataFrame(item_dict)
    item_df = df.set_index("item")

    item_date = item_df.loc[item]["date"]
    item_price = item_df.loc[item]["price"]
    item_name = item_df.loc[item]["name"]
    item_svg = item_df.loc[item]["svg"]
    # f'Item Name: {item_name}, Date: {item_date}, Price: {item_price}'

    #############################################
    # End Internal Item Call
    #############################################

    #############################################
    # Internal Coin Call
    #############################################

    # Convert JSON to DataFrame
    # coin_url_internal = "http://localhost:5000/coin"
    # coin_response_internal = requests.get(url_internal).json()
    # coin_response_internal = json.dumps(coin_response_internal)
    # coin_response_internal = json.loads(coin_response_internal)
    # coin_data = coin_response_internal
    # coin_df = pd.DataFrame.from_dict(coin_data, orient='columns')
    # coin_df = coin_df.set_index("time_period_start")

    # Get coin data from JSON raw file
    # Attempting to use direct JSON file and Pandas
    filepath = os.path.join("temp", "coin.json")
    with open(filepath) as jsonfile:
        coin_json = json.load(jsonfile)

    coin_file_df = pd.DataFrame(coin_json)
    coin_file_df = coin_file_df.set_index("time_period_start")
    # coin_file_df.head()

    # Match Item to Coin Price
    coin_date = item_date[:10]
    # f'Coin_date: {coin_date}'

    # Account for Pizza
    if item == "pizza":
        btc_price_on_item_day = 0.003
    else:
        btc_price_on_item_day = coin_file_df.loc[coin_date]["price_close"]

    # btc_price_on_item_day = coin_file_df.loc[coin_date]["price_close"]
    # f'Bitcoin price on item day: {btc_price_on_item_day}'

    # Quantity of Bitcoin for Price of Item
    bitcoin_shares = item_price / btc_price_on_item_day
    # f'Bitcoin Shares: {bitcoin_shares}'

    # ==========
    # Item Quantity at Max Bitcoin
    # Account for Cigarettes
    if item == "cigs":
        item_quantity_max = (((item_df.loc["bitcoin_max"]["price"])*bitcoin_shares)/item_price)*365/100
    else:
        item_quantity_max = ((item_df.loc["bitcoin_max"]["price"])*bitcoin_shares)/item_price

    # f'Maximum Item Quantity: {item_quantity_max}'
    print("Item Quantity Max")

    # ==========
    # Item Quantity Today
    today = datetime.datetime.now() - datetime.timedelta(hours = 80)
    today = today.isoformat()

    # Trim today for CoinAPI.io
    today = today[:19]
    # Trim today for Coin JSON
    today = today[:10]

    bitcoin_price_today = coin_file_df.loc[today]['price_close']
    print("Bitcoin Price Today")
    print(bitcoin_price_today)

    # Accountn for Cigs
    if item == "cigs":
        item_quantity_current = ((bitcoin_price_today*bitcoin_shares)/item_price)*365/100
    else:
        item_quantity_current = (bitcoin_price_today*bitcoin_shares)/item_price

    # f'Maximum Item Quantity: {item_quantity_current}'
    print("Item Quantity Current")
    print(item_quantity_current)
    #############################################
    # End Internal Coin Call
    #############################################


    ###############
    # For Database
    final_list = []
    dict_final = {}

    dict_final['item_name'] = item_name
    dict_final['item_date'] = item_date
    dict_final['item_price'] = item_price
    dict_final['bitcoin_shares'] = bitcoin_shares
    dict_final['bitcoin_price_today'] = bitcoin_price_today
    dict_final['btc_price_on_item_day'] = btc_price_on_item_day
    dict_final['item_quantity_max'] = item_quantity_max
    dict_final['item_quantity_current'] = item_quantity_current
    dict_final['item_svg'] = item_svg

    final_list.append(dict_final)

    # print(final_lst)
    quantity_item_df = pd.DataFrame(final_list)
    # print(quantity_item_df)
    # from sqlalchemy import create_engine
    engine2 = create_engine('sqlite://', echo=False)

    # engine = create_engine("sqlite:///../database.sqlite")

    quantity_item_df.to_sql('item_quantity_tbl', con=engine2)

    results = engine2.execute("SELECT * FROM item_quantity_tbl").fetchall()

    ###############

    return jsonify(final_list)






#################################################
# Extra Items
#################################################
@app.route("/itemstoo")
def list_items_too():
    item_dict_too = [
    {
        "item": "bitcoin_max",
        "name": "Bitcoin Peak",
        "date": "2017-12-17T20:00:00",
        "price": 19783.06,
        "svg": "static/images/bitcoin.svg",
        "bitcoin_price": 18961.0
    },{
        "item": "ps4",
        "name": "PS4",
        "date": "2013-11-15T20:00:00",
        "price": 399,
        "svg": "static/images/playstation-logo.svg",
        "bitcoin_price": 412.0
    },{
        "item": "macbook",
        "name": "MacBook Pro 2012",
        "date": "2012-07-30T20:00:00",
        "price": 1199,
        "svg": "static/images/laptop.svg",
        "bitcoin_price": 9.0979
    },{
        "item": "oculus",
        "name": "Oculus Rift",
        "date": "2016-03-28T20:00:00",
        "price": 599,
        "svg": "static/images/oculus-rift-virtual-reality-svgrepo-com.svg",
        "bitcoin_price": 419.995
    },{
        "item": "fiftycent",
        "name": "50 Cent",
        "date": "2014-02-11T20:00:00",
        "price": 400000,
        "svg": "static/images/50cent-cd.svg",
        "bitcoin_price": 664.666
    },{
        "item": "cigs",
        "name": "365 Packs of Cigarettes in 2014",
        "date": "2014-12-31T20:00:00",
        "price": 1989.25,
        "svg": "static/images/cigarette-box-lighter.svg",
        "bitcoin_price": 317.000
    }]
    return jsonify(item_dict_too)


#################################################
# Flask Last part of Setup
#################################################
if __name__ == "__main__":
    app.run(debug=True)
    # app.run()