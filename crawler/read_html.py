import pandas as pd
import requests
from bs4 import BeautifulSoup
url = "https://www.swimmingrank.com/zone/usa/scy_girls_5_8_50FR.html"
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
table = soup.find_all('table')[0]
df = pd.read_html(str(table), header=0, index_col=0)[0]

from sqlalchemy import create_engine
import sqlite3
engine = create_engine('sqlite:////Users/alexren/projects/projectX/db')
df.index.names = ['id']
df = df.rename({'Swim Meet': 'Swim_Meet'}, axis=1)
df.to_sql('US_Rankings', con=engine, if_exists='replace')
print(df)