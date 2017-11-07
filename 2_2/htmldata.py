from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

# Author: tuomas.granlund@solita.fi
# 07.11.2017

# GDP_(PPP)
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(PPP)_per_capita"
html = urlopen(url)
soup = BeautifulSoup(html, "lxml")
table = soup.findAll('table', limit=2)[1]
data_rows = table.findAll('tr')[1:]
list_data = []
countries = []
gdp = []
for i in range(len(data_rows)):
    row = data_rows[i].findAll('td')[1:]
    list_data.append([row[0].findAll('a').pop(0).getText(), row[1].getText()])
    countries.append(row[0].findAll('a').pop(0).getText())
    gdp.append(row[1].getText())

df_gdp = pd.DataFrame(gdp, index=countries, columns=['GDP (PPP) per capita'])

# Happiness score
hs = pd.read_html("https://en.wikipedia.org/wiki/World_Happiness_Report")
hs = hs.pop(0)
hs.drop(hs.columns[[0, 1, 4, 5, 6, 7, 8, 9, 10, 11]], axis=1, inplace=True)
hs = hs.iloc[1:]
hs.set_index(2, inplace=True)

# Merge gdp and happiness
df_gdp_happiness = pd.merge(df_gdp, hs, left_index=True, right_index=True)
df_gdp_happiness.rename(columns={3: 'Happiness score'}, inplace=True)

print(df_gdp_happiness)

