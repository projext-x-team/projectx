'''
This module is to download the US Ranking data from web sites and saved it into database
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

import datetime
import numbers


from config import *
from US_RankingsModel import *

DB_URI = Config.DB_URI

db = SQLAlchemy(app)

# delete all of the rows from the existing table
engine=  create_engine(DB_URI)
meta = MetaData(bind=engine, reflect=True)
con = engine.connect()
trans = con.begin()
#con.execute('SET FOREIGN_KEY_CHECKS = 0;')
for table in meta.sorted_tables:
    if str(table.name) == 'US_Rankings':
        con.execute(table.delete())
#con.execute('SET FOREIGN_KEY_CHECKS = 1;')
trans.commit()

# the base_url shows 5 zones: Central, Eastern, Southern, Western and USA
# we only need the first 4 zones: Central, Eastern, Southern, Western
base_url = "https://www.swimmingrank.com/zone/select_zone.html"
zones=["central", "eastern", "southern", "western"]

# get short course or long course information from the URL
def getCourse(url):
    # a url should be like https://www.swimmingrank.com/zone/western/lcm_boys_all.html
    if url.split("/")[-1].split('_')[0]=='lcm':
        ret="Long Course"
    else:
        ret="Short Course"
    return ret

def getAgeGp(url):
    # a url should be like https://www.swimmingrank.com/zone/western/lcm_boys_all.html 
    # or https://www.swimmingrank.com/zone/western/lcm_boys_17_18.html
    arr=url.split("/")[-1].split('.')[0].split('_')
    if len(arr)<4:
        ret="All Age"
    else:
        ret=arr[2]+"_"+arr[3]
    return ret

class AgeGroup:
    # class to map to https://www.swimmingrank.com/zone/central/select_age.html
    zone=""
    ageGp=""
    gender=""
    url=""
    course=""

class SwimEvent:
    # class to map to https://www.swimmingrank.com/zone/central/scy_girls_5_8.html
    eventName=""    #100IM, etc
    ranking="" # Current Season Ranking or Career Best Ranking
    res=""
    soup=""
    buttons=[]

class Result:
    # class to map to https://www.swimmingrank.com/zone/central/scy_girls_5_8_50FR.html
    res=""
    soup=""
    table=""


# main program starts here
total_records=0
for zone in zones:
    zone_url="https://www.swimmingrank.com/zone/"+zone+"/select_age.html"
    print(zone_url)
    # from the zone url, we will get all of the urls for age group, short/long course and gender
    res=requests.get(zone_url)
    soup=BeautifulSoup(res.content, 'html.parser')
    buttons=soup.find_all('button')
    for button in buttons:
        ageGroup=AgeGroup()
        ageGroup.zone=zone
        ageGroup.gender=button.get_text()
        ageGroup.url=button.get('onclick').split("=")[1]
        ageGroup.ageGp=getAgeGp(ageGroup.url)
        ageGroup.course=getCourse(ageGroup.url)
        print(ageGroup.gender+ "->"+ ageGroup.ageGp + "->"+ ageGroup.course + "->"+ ageGroup.url)
        # from each zone's age group, "Long/Short Course" and gender, get All events
        swimEvent=SwimEvent()
        swimEvent.res=requests.get(ageGroup.url[1:-1]) # remove the quotes from the url string
        swimEvent.soup=BeautifulSoup(swimEvent.res.content, 'html.parser')
        div=swimEvent.soup.find_all('table')
        swimEvent.buttons=div[0].find_all('button')
        career_best=False
        for swimEventButton in swimEvent.buttons:
            career_best=not career_best
            swimEvent.event=swimEventButton.get_text()
            swimEvent.url=swimEventButton.get('onclick').split("=")[1]
            print(str(career_best)+"->"+swimEvent.event+"->"+swimEvent.url)
            if career_best:
                swimEvent.ranking="Career Best Ranking"
            else:
                swimEvent.ranking="Current Season Ranking"
            # get final results from a page like https://www.swimmingrank.com/zone/central/scy_girls_5_8_50FR.html
            print(swimEvent.url[1:-1])
            result=Result()
            result.res = requests.get(swimEvent.url[1:-1])
            result.soup = BeautifulSoup(result.res.content, 'html.parser')
            result.table = result.soup.find_all('table')[0]
            df = pd.read_html(str(result.table), header=0, index_col=0)[0]
            for r in df.to_dict('records'):
                print(r)
                if career_best:
                    tempAge=r['Age']
                else:
                    tempAge=r['Current Age']
                if (str(r['Time'])).find(":") > 0:
                    tempTime=datetime.datetime.strptime(str(r['Time']),"%M:%S.%f")
                else:
                    tempTime=datetime.datetime.strptime(str(r['Time']),"%S.%f")
                swimmer=US_Rankings(
                        swimmer=r['Swimmer'],
                        age=tempAge,
                        club=r['Club'],
                        lsc=r['LSC']  ,          #IN, LE, MI
                        gender=ageGroup.gender,    # girl, boy
                        zone=ageGroup.zone,      # Central, Western, etc
                        ageGp=ageGroup.ageGp,    #17-18, all, etc
                        event=swimEvent.event,  #100IM, etc
                        ranking=swimEvent.ranking,   # Current Season or Career Best
                        course=ageGroup.course,  # Short course, long course
                        time=tempTime,
                        date=datetime.datetime.strptime(str(r['Date']),"%m/%d/%y"),
                        swim_meet=r['Swim Meet']
                    )
                db.session.add(swimmer)
                total_records+=1
        db.session.commit()
        if Config.ENV=="dev" and total_records >= 1000:
                    quit()

