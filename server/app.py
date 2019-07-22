from flask import Flask, render_template, url_for, jsonify, request, Response, redirect, flash
from functools import wraps
import json, jwt, datetime

from config import *
from SwimmerModel import *
from US_RankingsModel import *
from SearchSwimmerForm import SearchSwimmerForm

swimmers = Swimmer.get_all_swimmers()
swimmers_added = []

def add_swimmers(_swimmer, swimmername):
    if _swimmer == {}:
        flash(swimmername + " can't be found")
        app.logger.debug(swimmername + " can't be found")
        return
    for swimmer in swimmers_added:
        if swimmer['name'] == _swimmer['name']:
            flash(swimmername + " is already added")
            app.logger.debug(swimmername + "is already added")
            return
    flash(swimmername + " is added")
    swimmers_added.append(dict(_swimmer))



@app.route("/")
@app.route("/index")
def home():
    return render_template("index.html", title = Config.AppName, topSwimmers=US_Rankings.topSwimmers(100))

@app.route("/times-search", methods=["GET","POST"])
def search_swimmers_by_name():
    form = SearchSwimmerForm()
    if form.validate_on_submit():
        swimmername=form.swimmername.data
        add_swimmers(Swimmer.get_swimmer_by_name(swimmername), swimmername)
        app.logger.debug(str(swimmers_added))
        return redirect(url_for('search_swimmers_by_name'))
    return render_template("times_search.html", form=form, swimmers_added=swimmers_added)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)