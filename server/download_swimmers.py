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

class Result:
    # store downloaded web page
    res=""
    soup=""
    div=""
    table=""


# main program starts here

'''
for i in ascii_lowercase:
    for j in ascii_lowercase:
        post_params = { 
            'searchstring'  : i+j   # search name like "aa", "ab", till "zz"
            }
'''
post_params = { 
    'searchstring'  : "alex ren"   # search name like "aa", "ab", till "zz"
    }
data = urllib.parse.urlencode(post_params).encode("utf-8")
req = urllib.request.Request(base_url)
swimmer=Swimmer()
with urllib.request.urlopen(req,data=data) as f:
    resp = f.read()
    soup=BeautifulSoup(resp, 'html.parser')
    table=soup.find_all('table')[0]
    buttons=table.find_all('button')
    #print(buttons)
    for button in buttons:
        swimmer.name = button.get_text()
        swimmer.swimmer_uuid = uuid.uuid4().hex
        url=button.get('onclick').split("=")[1]
        #print(swimmer.name + " ->" +url)
        result=Result()
        result.res = requests.get(url[1:-1])
        result.soup = BeautifulSoup(result.res.content, 'html.parser')
        #print(result.soup)
        result.div = result.soup.find(id="content")
        #print(result.div)
        result.tables = result.div.find_all('table')
        #print(result.tables)
        #for table in result.tables:
        for i in range(len(result.tables)):
            df = pd.read_html(str(result.tables[i]), header=0, index_col=0)[0]
            app.logger.debug("======= Table #"+str(i))
            # one swimmer
            if i==0:
                # the first table shows the swimmer information
                r=df.to_dict('records')[0] # the first row: {'Pleasanton Seahawks': 'Zone 2', 'Latest Meets': 'Zone 2'}
                app.logger.debug("xxxxxx")
                app.logger.debug(df)
                app.logger.debug("xxxxxx")
                swimmer.club=list(r.keys())[0] 
                swimmer.age=df.loc['Age','Latest Meets']
                swimmer.gender=df.loc['Sex','Latest Meets']
                swimmer.lsc=df.loc['LSC','Latest Meets']
            else:
                # the second and later tables show the swimmer meet results
                if len(df.to_dict())>0:
                    r=df.to_dict()
                    k1=list(r.keys())[0]
                    swimmer.swim_meet=k1.split(".")[0]
                    if len(r[k1].keys()) > 0 :
                        print(r[k1].keys())
                        k11=list(r[k1].keys())[0]
                        swimmer.meet_date=k11.split("Age")[0]
                        swimmer.meet_age=k11.split("Age")[1]
                        for j in range(2, len(r[k1].keys())):
                            swimmer.event=list(r[k1].keys())[j]
                            swimmer.time=r[k1][swimmer.event]
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





