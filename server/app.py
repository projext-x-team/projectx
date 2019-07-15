from flask import Flask, render_template, url_for, jsonify, request, Response, redirect, flash
from functools import wraps
import json, jwt, datetime

from config import *
from SwimmerModel import *

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

@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html", title = Config.AppName, topSwimmers=US_Rankings.topSwimmers(100))

@app.route("/compare")
def swimmer_search():
    return render_template("compare.html", title = Config.AppName)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)