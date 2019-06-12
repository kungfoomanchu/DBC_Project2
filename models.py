from .flaskcode import db

class coinsDB(db.Model):
    __tablename__ = 'coin' 
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    coin_name = db.Column(db.String(64))
    time_start = db.Column(db.String(64))
    price_close = db.Column(db.String(64))
    
    
    def __repr__(self):
        return '<coinsDB %r>' % (self.coin_name)

@app.before_first_request
def setup():
    # Recreate database each time for demo
    db.drop_all()
    db.create_all()