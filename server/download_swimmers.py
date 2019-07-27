'''
This module is to download the swimmer data from web sites and saved it into database
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *
from string import *

import datetime
import numbers
import urllib
import json
import copy
import uuid


from config import *
from SwimmerModel import *

DB_URI = Config.DB_URI

db = SQLAlchemy(app)

'''
# delete all of the rows from the existing table
engine=  create_engine(DB_URI)
meta = MetaData(bind=engine, reflect=True)
con = engine.connect()
trans = con.begin()
#con.execute('SET FOREIGN_KEY_CHECKS = 0;')
for table in meta.sorted_tables:
    if str(table.name) == 'swimmers':
        con.execute(table.delete())
#con.execute('SET FOREIGN_KEY_CHECKS = 1;')
trans.commit()
'''

base_url = "https://swimmingrank.com/cgi-bin/ca_search.cgi"

class SwimmerResult:
    # store downloaded web page
    res=""
    soup=""
    div=""
    table=""
    eventmenu=""
    urls=""

class SwimmerEventResult:
    res=""
    soup=""
    div=""
    table=""
    h3=""

# main program starts here

'''
for i in ascii_lowercase:
    for j in ascii_lowercase:
        post_params = { 
            'searchstring'  : i+j   # search name like "aa", "ab", till "zz"
            }
'''
post_params = { 
    'searchstring'  : "ethan wang"   
    }
data = urllib.parse.urlencode(post_params).encode("utf-8")
req = urllib.request.Request(base_url)
swimmer=Swimmer()
with urllib.request.urlopen(req,data=data) as f:
    resp = f.read()
    soup=BeautifulSoup(resp, 'html.parser')
    table=soup.find_all('table')[0]
    buttons=table.find_all('button')
    
    # each button has one swimmer name
    for button in buttons:
        swimmer.name = button.get_text()
        swimmer.swimmer_uuid = uuid.uuid4().hex
        url=button.get('onclick').split("=")[1]
        
        # read data from swimmer's page like https://www.swimmingrank.com/cal/strokes/strokes_pc/AILOEARCE_meets.html
        swimmerResult=SwimmerResult()
        swimmerResult.res = requests.get(url[1:-1])
        swimmerResult.soup = BeautifulSoup(swimmerResult.res.content, 'html.parser')
        #print(swimmerResult.soup)
        swimmerResult.div = swimmerResult.soup.find(id="content")
        swimmerResult.tables = swimmerResult.div.find_all('table')
        #tables[0] has the swimmer information
        df = pd.read_html(str(swimmerResult.tables[0]), header=0, index_col=0)[0]
        r=df.to_dict('records')[0] # the first row: {'Pleasanton Seahawks': 'Zone 2', 'Latest Meets': 'Zone 2'}
        swimmer.club=list(r.keys())[0] 
        swimmer.age=df.loc['Age','Latest Meets']
        swimmer.gender=df.loc['Sex','Latest Meets']
        swimmer.lsc=df.loc['LSC','Latest Meets']

        swimmerResult.eventmenu = swimmerResult.soup.find(id="event_menu")
        swimmerResult.urls = swimmerResult.eventmenu.find_all('a', href=True)
        for i in range(1, len(swimmerResult.urls)):
            # from the Nav bar, get all of the events URLs
            url=swimmerResult.urls[i]['href'] # sample: https://www.swimmingrank.com/cal/strokes/strokes_pc/AILOEARCE_50FR.html
            app.logger.debug(url)
            swimmerEventResult=SwimmerEventResult()
            swimmerEventResult.res = requests.get(url)
            swimmerEventResult.soup=BeautifulSoup(swimmerEventResult.res.content, 'html.parser')
            selector = 'h3'
            h3s=swimmerEventResult.soup.select(selector)
            selector = 'h3 ~ table'
            tables=swimmerEventResult.soup.select(selector)
            for i in range(len(tables)-1):  # the last table is "About Us", which we don't need
                df = pd.read_html(str(tables[i]))[0]
                if len(df.to_dict())>0:
                    r=df.to_dict()
                    app.logger.debug("-------------------------------")
                    app.logger.debug(h3s[i].text)
                    app.logger.debug(len(df.columns))
                    app.logger.debug(df.keys)
                    app.logger.debug(df.items)
                    app.logger.debug(df.index)
                    # iterate through the table to get swim data
                    for j in df.index:
                        app.logger.debug(df.loc[j, "Swim Meet"])
                        swimmer.swim_meet=df.loc[j, "Swim Meet"]
                        swimmer.meet_date=df.loc[j, "Date"]
                        swimmer.meet_age=int(df.loc[j, "Age"])
                        swimmer.event=h3s[i].text
                        swimmer.time=df.loc[j, "Time"]
                        swimmer.standard=df.loc[j,"Standard"]
                        swimmer.swim_team=df.loc[j,"Swim Team"]
                        if (str(swimmer.time)).find(":") > 0:
                            tempTime=datetime.datetime.strptime(str(swimmer.time),"%M:%S.%f")
                        else:
                            tempTime=datetime.datetime.strptime(str(swimmer.time),"%S.%f")
                        swimmer.time=tempTime
                        swimmer.time_h=tempTime.hour
                        swimmer.time_m=tempTime.minute
                        swimmer.time_s=tempTime.second
                        swimmer.time_ms=tempTime.microsecond
                        swimmer_record=Swimmer()
                        swimmer_record=copy.deepcopy(swimmer)
                        #app.logger.debug(swimmer_record)
                        db.session.add(swimmer_record)
                        db.session.commit()

                