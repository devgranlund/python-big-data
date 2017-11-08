from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import matplotlib.pyplot as plt
import locale

# Author: tuomas.granlund@solita.fi
# 07.11.2017

locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

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
    gdp.append(int(locale.atoi(row[1].getText())))

df_gdp = pd.DataFrame(gdp, index=countries, columns=['GDP (PPP) per capita'])

# Happiness score
hs = pd.read_html("https://en.wikipedia.org/wiki/World_Happiness_Report")
hs = hs.pop(0)
hs.drop(hs.columns[[0, 1, 4, 5, 6, 7, 8, 9, 10, 11]], axis=1, inplace=True)
hs = hs.iloc[1:]
hs.set_index(2, inplace=True)

# merge gdp and happiness
df_gdp_happiness = pd.merge(df_gdp, hs, left_index=True, right_index=True)
df_gdp_happiness.rename(columns={3: 'Happiness score'}, inplace=True)

# Life expectancy
le = pd.read_html("https://en.wikipedia.org/wiki/List_of_countries_by_life_expectancy")
le = le.pop(0)
le.drop(le.columns[[1, 3, 4, 5, 6, 7, 8]], axis=1, inplace=True)
le = le.iloc[1:]
le.set_index(0, inplace=True)

# merge le to df_gdp_happiness
df_gdp_happiness_life = pd.merge(df_gdp_happiness, le, left_index=True, right_index=True)
df_gdp_happiness_life.rename(columns={2: 'Life expectancy'}, inplace=True)

# Birth rate
url = "https://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_by_birth_rate"
html = urlopen(url)
soup = BeautifulSoup(html, "lxml")
table = soup.findAll('table', limit=2)[1]
data_rows = table.findAll('tr')[3:]
countries = []
br = []
for i in range(196):
    row = data_rows[i].findAll('td')
    countries.append(row[0].findAll('a').pop(0).getText())
    br.append(row[9].getText())

df_br = pd.DataFrame(br, index=countries, columns=['Birth rate'])

# merge df_br to df_gdp_happiness_life_br
df_gdp_happiness_life_br = pd.merge(df_gdp_happiness_life, df_br, left_index=True, right_index=True)

# Write data to HTML
html = df_gdp_happiness_life_br.to_html()
file = codecs.open('countrydata.html', "w", "utf-8")
file.write(html)
file.close()

# Scatter plots
df = df_gdp_happiness_life_br  # for convenience
df[['GDP (PPP) per capita', 'Happiness score', 'Life expectancy', 'Birth rate']] = \
    df[['GDP (PPP) per capita', 'Happiness score', 'Life expectancy', 'Birth rate']].apply(pd.to_numeric)

plt.figure(1, figsize=(10, 10))

# gdp vs happiness
plt.subplot(321)
plt.scatter(df['GDP (PPP) per capita'], df['Happiness score'], s=2)
plt.xlabel('GDP (PPP) per capita')
plt.ylabel('Happiness score')

# gdp vs life expectancy
plt.subplot(322)
plt.scatter(df['GDP (PPP) per capita'], df['Life expectancy'], s=2)
plt.xlabel('GDP (PPP) per capita')
plt.ylabel('Life expectancy')

# gdp vs birth rate
plt.subplot(323)
plt.scatter(df['GDP (PPP) per capita'], df['Birth rate'], s=2)
plt.xlabel('GDP (PPP) per capita')
plt.ylabel('Birth rate')

# happiness vs life expectancy
plt.subplot(324)
plt.scatter(df['Happiness score'], df['Life expectancy'], s=2)
plt.xlabel('Happiness score')
plt.ylabel('Life expectancy')

# happiness vs birth rate
plt.subplot(325)
plt.scatter(df['Happiness score'], df['Birth rate'], s=2)
plt.xlabel('Happiness score')
plt.ylabel('Birth rate')

# life expectancy vs birth rate
plt.subplot(326)
plt.scatter(df['Life expectancy'], df['Birth rate'], s=2)
plt.xlabel('Life expectancy')
plt.ylabel('Birth rate')

plt.subplots_adjust(top=0.98, bottom=0.02)
# plt.show()
plt.savefig('countryplots.png')
