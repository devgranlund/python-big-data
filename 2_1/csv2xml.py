import pandas
import codecs
from bs4 import BeautifulSoup

# Author: tuomas.granlund@solita.fi
# 06.11.2017

# read data from csv and insert column names
populationData = pandas.read_csv('population.csv', delimiter=';', skiprows=4,
                                 names=['name', 'year', 'total', 'males', 'females'])

# create object for xml
soup = BeautifulSoup(features='xml')
root = soup.new_tag("populationdata")
soup.append(root)

# iterate over data and populate xml object
for index, row in populationData.iterrows():
    municipalityTag = soup.new_tag("municipality")
    nameTag = soup.new_tag("name")
    nameTag.string = row['name']
    municipalityTag.append(nameTag)
    yearTag = soup.new_tag("year")
    yearTag.string = str(row['year'])
    municipalityTag.append(yearTag)
    totalTag = soup.new_tag("total")
    totalTag.string = str(row['total'])
    municipalityTag.append(totalTag)
    malesTag = soup.new_tag("males")
    malesTag.string = str(row['males'])
    municipalityTag.append(malesTag)
    femalesTag = soup.new_tag("females")
    femalesTag.string = str(row['females'])
    municipalityTag.append(femalesTag)
    root.append(municipalityTag)

# create file and write
file = codecs.open("population.xml", "w", "utf-8")
file.write(soup.prettify())
file.close()
