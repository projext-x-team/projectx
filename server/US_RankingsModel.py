from flask_sqlalchemy import SQLAlchemy
from config import app
import json

db = SQLAlchemy(app)

class US_Rankings(db.Model):
    __tablename__ = 'US_Rankings'
    id = db.Column(db.BigInteger, primary_key = True)
    swimmer = db.Column(db.Text)
    age = db.Column(db.BigInteger)
    lsc = db.Column(db.Text)
    club = db.Column(db.Text)
    time = db.Column(db.Float)
    date = db.Column(db.Text)
    swim_meet = db.Column(db.Text)

    @staticmethod
    def topSwimmers(num):
        return US_Rankings.query.order_by(US_Rankings.time.asc()).limit(num)

    def __repr__(self):
        return "<US_Rankings: {}>".format(self.swimmer)