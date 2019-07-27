from flask_sqlalchemy import SQLAlchemy
from config import app
import json

db = SQLAlchemy(app)

class US_Rankings(db.Model):
    __tablename__ = 'US_Rankings'
    id = db.Column(db.Integer, primary_key = True)
    swimmer = db.Column(db.String)
    age = db.Column(db.BigInteger)
    gender = db.Column(db.String)
    zone = db.Column(db.String)
    ageGp = db.Column(db.String)
    lsc = db.Column(db.String)
    club = db.Column(db.String)
    event = db.Column(db.String)
    ranking = db.Column(db.String)
    course = db.Column(db.String)
    time = db.Column(db.DateTime)
    date = db.Column(db.DateTime)
    swim_meet = db.Column(db.String)

    @staticmethod
    def topSwimmers(num):
        return US_Rankings.query.order_by(US_Rankings.time.asc()).limit(num)

    def __repr__(self):
        return "<US_Rankings: {}>".format(self.swimmer)