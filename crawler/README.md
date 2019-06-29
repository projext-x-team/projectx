```
import pandas as pd
import requests
from bs4 import BeautifulSoup

res = requests.get("http://www.nationmaster.com/country-info/stats/Media/Internet-users")
soup = BeautifulSoup(res.content,'lxml')
table = soup.find_all('table')[0] 
df = pd.read_html(str(table))
print(df[0].to_json(orient='records'))
```
```
res = requests.get("https://www.swimmingrank.com/index.html")
soup = BeautifulSoup(res.content, 'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))
print(df[0].to_json(orient='records'))
```
```
res = requests.get("http://www.pacswim.org/")
soup = BeautifulSoup(res.content, 'lxml')
table = soup.find_all('table')
df = pd.read_html(str(table))
for i in range(len(df)):
    print(df[i].to_json(orient = 'records'))
```
```
res = requests.get("https://www.swimmingrank.com/cal/index.html")
soup = BeautifulSoup(res.content, 'lxml')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))
print(df[0].to_json(orient='records'))
```
