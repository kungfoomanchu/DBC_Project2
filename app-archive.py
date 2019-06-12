from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)
from flask_pymongo import PyMongo
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy
import price_calc_flask

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db/coins.sqlite"

db = SQLAlchemy(app)

class Coin(db.Model):
    __tablename__ = 'coins'

    id = db.Column(db.Integer, primary_key=True)
    coinName = db.Column(db.String(64))
    date = db.Column(db.String)
    price_close = db.Column(db.Integer)

    def __repr__(self):
        return '<Coin %r>' % (self.name)

@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()


# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")


# Query the database and send the jsonified results
@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        coinName = request.form["coinName"]
        date = request.form["date"]
        price_close = 992.95

        coin = Coin(name=coinName, date=date, price_close=price_close)
        db.session.add(coin)
        db.session.commit()
        return redirect("/", code=302)

    return render_template("form.html")

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

if __name__ == "__main__":
    app.run(debug=True)