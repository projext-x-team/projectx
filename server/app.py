from flask import Flask, render_template, url_for, jsonify, request, Response, redirect, flash
from functools import wraps
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.layouts import column, gridplot
from bokeh.embed import components
from bokeh.palettes import Plasma5 
from bokeh.models import Legend
from bokeh.models import DatetimeTickFormatter
import pandas as pd
import json, jwt, datetime
from math import pi
from datetime import datetime

from config import *
from SwimmerModel import *
from US_RankingsModel import *
from SearchSwimmerForm import SearchSwimmerForm

swimmers = Swimmer.get_all_swimmers()
swimmers_added = []
swimmers_added_alldata = []
plots = []

# define the primary swimmer based on user selection
def set_primary_swimmer():
    if len(swimmers_added) == 0:
        return "Checked"
    else:
        for swimmer in swimmers_added:
            if swimmer['primary'] == "Checked":
                return ""
        return "Checked"

def set_compare_swimmer():
    return "Checked"

# add new swimmers to compare
def add_swimmers(_swimmers, swimmername):
    if len(_swimmers) == 0:
        flash(swimmername + " can't be found")
        return
    for swimmer in swimmers_added:
        if swimmer['name'].lower() == swimmername.lower():
            flash(swimmername + " is already added")
            return
    flash(swimmername + " is added")
    swimmers_added_alldata.extend(_swimmers)
    for _swimmer in _swimmers:
        bExisting=False
        for swimmer_added in swimmers_added:
            if swimmer_added['name'] == _swimmer['name'] and swimmer_added['age'] == _swimmer['age'] and swimmer_added['club'] == _swimmer['club']:
                bExisting = True
                break
        if not bExisting:
            s={
                'id': _swimmer['id'],
                'swimmer_uuid': _swimmer['swimmer_uuid'],
                'name': _swimmer['name'],
                'age': int(_swimmer['age']),
                'club': _swimmer['club'],
                'primary': set_primary_swimmer(),
                'compare': set_compare_swimmer() # set 'compare' as "checked" as default
            }
            swimmers_added.append(s)



#@app.route("/")
#@app.route("/index")
def home():
    return render_template("index.html", title = Config.AppName, topSwimmers=US_Rankings.topSwimmers(100))

@app.route("/", methods=["GET","POST"])
@app.route("/index", methods=["GET","POST"])
@app.route("/times-search", methods=["GET","POST"])
def search_swimmers_by_name():
    form = SearchSwimmerForm()
    if form.validate_on_submit():
        swimmername=form.swimmername.data
        add_swimmers(Swimmer.get_swimmer_by_name(swimmername), swimmername)
        plots.append(make_plot())
        return redirect(url_for('search_swimmers_by_name'))
    return render_template("times_search.html", form=form, swimmers_added=swimmers_added, plots=plots)

def make_plot():
    df_swimmers=pd.DataFrame(swimmers_added)
    df_swimmers_data=pd.DataFrame(swimmers_added_alldata)

    primary_swimmer=df_swimmers[df_swimmers.primary=="Checked"]
    compared_swimmers=df_swimmers[df_swimmers.compare=="Checked"]

    primary_swimmer_data=df_swimmers_data[df_swimmers_data.swimmer_uuid==primary_swimmer.swimmer_uuid[0]]
    primary_swimmer_data['meet_date'] = primary_swimmer_data['meet_date'].astype('datetime64[ns]')
    primary_swimmer_data=primary_swimmer_data.sort_values(by=['event', 'meet_date'])

    events=list(set(primary_swimmer_data.event))
    events.sort()
    plots=[]
    for e in events:
        legend_list = []
        tooltips = [
            ("Name", "@name"),
            ("Swim Meet", "@swim_meet"),
            ("Date", "@meet_date"),
            ("At age", "@age"),
            ("Result", "@result")
        ]

        p = figure( y_axis_type="datetime", plot_height=250, sizing_mode="scale_width", tooltips=tooltips, title=e)
        #add data to existing plot for every swimmer
        for index, swimmer in compared_swimmers.iterrows():
            compared_swimmer_data=df_swimmers_data[df_swimmers_data.swimmer_uuid==swimmer.swimmer_uuid]
            compared_swimmer_data['meet_date'] = compared_swimmer_data['meet_date'].astype('datetime64[ns]')
            compared_swimmer_data=compared_swimmer_data.sort_values(by=['event', 'meet_date'])

            data = compared_swimmer_data[compared_swimmer_data.event==e]

            if data.empty == False:
                # data['swim_meet_date'] = data['swim_meet']+ " " + data['meet_date'].astype(str)
                #x = pd.to_datetime(data['meet_date'], format="%y/%m/%d")
                x = data['meet_age']
                y = pd.to_datetime(data['time'], format="%M:%S.%f")

                source = ColumnDataSource(data=dict(
                    x=x,
                    y=y,
                    name=data['name'],
                    swim_meet=data['swim_meet'],
                    meet_date=data['meet_date'].astype(str),
                    age=data['meet_age'],
                    result=data['time']
                ))

                p.xaxis.major_label_orientation= "vertical"
                '''
                p.xaxis.formatter=DatetimeTickFormatter(
                        years = ['%m / %d / %Y'],
                        months = ['%m / %d / %Y'],
                        days = ['%m / %d / %Y'],
                    )
                '''
                p.yaxis.formatter=DatetimeTickFormatter(
                        minutes = ['%M:%S.%3N'],
                        seconds = ['%M:%S.%3N'],
                        milliseconds = ['%M:%S.%3N'],
                    )
                line = p.line('x', 'y', line_width=2, source=source, line_color=Plasma5[index%5])
                circle = p.circle('x','y', size=5, color=Plasma5[index%5], source=source)
                legend_list.append((data['name'].iloc[0], [circle, line]))

        legend = Legend(items=legend_list, location="top_right")
        p.add_layout(legend, 'right')
        p.xaxis.axis_label = "Age"
        p.yaxis.axis_label = "Time"
        plots.append(p)
    

    # plots is a simple list [p1, p2, p3, p4 ....]
    # convert plots to [[p1, p2], [p3, p4], ...]
    ps=[]
    for i in range(int(len(plots)/2)):
        ps.append([plots[i*2],plots[i*2+1]])
    if len(plots) % 2 ==1:  # if plots has odd number
        ps=ps.append([plots[len(plots)-1],None])
    
    #script, div = components(column(plots))
    grid = gridplot(ps)
    script, div = components(grid)
    return script, div


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(debug=True)