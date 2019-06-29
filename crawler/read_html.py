import pandas as pd
import requests
from bs4 import BeautifulSoup
url = "https://www.swimmingrank.com/zone/usa/scy_girls_5_8_50FR.html"
res = requests.get(url)
soup = BeautifulSoup(res.content, 'html.parser')
table = soup.find_all('table')[0]
df = pd.read_html(str(table))
print(df)