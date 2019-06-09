from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from flask_pymongo import PyMongo
from sqlalchemy import func, create_engine
from flask_sqlalchemy import SQLAlchemy
import price_calc_flask

# For ItemQuantity
import requests
import pandas as pd
import datetime
from config import api_key

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
item_df



app = Flask(__name__)

engine = create_engine('sqlite://', echo=False)

item_df.to_sql('items_tbl', con=engine)
engine.execute("SELECT * FROM items_tbl").fetchall()
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/coins.sqlite"

# db = SQLAlchemy(app)

# class Coin(db.Model):
#     __tablename__ = 'coins'

#     id = db.Column(db.Integer, primary_key=True)
#     coinName = db.Column(db.String(64))
#     date = db.Column(db.String)
#     price_close = db.Column(db.Integer)

#     def __repr__(self):
#         return '<Coin %r>' % (self.name)





# Before first request

# @app.before_first_request
# def setup():
#     # Recreate database each time for demo
#     db.drop_all()
#     db.create_all()


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# # Query the database and send the jsonified results
# @app.route("/send", methods=["GET", "POST"])
# def send():
#     if request.method == "POST":
#         coinName = request.form["coinName"]
#         date = request.form["date"]
#         price_close = 992.95

#         coin = Coin(name=coinName, date=date, price_close=price_close)
#         db.session.add(coin)
#         db.session.commit()
#         return redirect("/", code=302)

#     return render_template("form.html")

# create route that returns data for plotting
# @app.route("/api/pals")
# def pals():
#     results = db.session.query(Pet.type, func.count(Pet.type)).group_by(Pet.type).all()

#     pet_type = [result[0] for result in results]
#     age = [result[1] for result in results]

#     trace = {
#         "x": pet_type,
#         "y": age,
#         "type": "bar"
#     }

#     return jsonify(trace)

@app.route("/quantity/<item>")
def get_quantity(item):
    item_date = item_df.loc[item]["date"]
    item_price = item_df.loc[item]["price"]
    item_name = item_df.loc[item]["name"]

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
    bitcoin_value_on_item_day = response[0]['price_close']
    print(bitcoin_value_on_item_day)

    # Quantity of Bitcoin for Price of Item
    bitcoin_shares = item_price / bitcoin_value_on_item_day
    print(bitcoin_shares)

    # ==========
    # Item Quantity at Max Bitcoin
    item_quantity_max = ((item_df.loc["bitcoin_max"]["price"])*bitcoin_shares)/item_price
    print(item_quantity_max)

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
    print(item_quantity_current)

    return f'You would have {item_quantity_max} {item_name}s if you sold at the peak. You would have {item_quantity_current} {item_name}s if you sold at the peak.'

if __name__ == "__main__":
    app.run(debug=True)