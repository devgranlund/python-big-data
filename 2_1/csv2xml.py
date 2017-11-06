import pandas
import codecs
import sys
from bs4 import BeautifulSoup


# Author: tuomas.granlund@solita.fi
# 06.11.2017

def read_csv_and_create_xml(input_file_name, output_file_name):

    # validate function arguments
    if input_file_name:
        csv_file = input_file_name
    else:
        csv_file = 'population.csv'
    if output_file_name:
        xml_file = output_file_name
    else:
        xml_file = "population.xml"

    # read data from csv and insert column names
    population_data = pandas.read_csv(csv_file, delimiter=';', skiprows=4,
                                      names=['name', 'year', 'total', 'males', 'females'])

    # create object for xml
    soup = BeautifulSoup(features='xml')
    root = soup.new_tag("populationdata")
    soup.append(root)

    # iterate over data and populate xml object
    for index, row in population_data.iterrows():
        municipality_tag = soup.new_tag("municipality")
        name_tag = soup.new_tag("name")
        name_tag.string = row['name']
        municipality_tag.append(name_tag)
        year_tag = soup.new_tag("year")
        year_tag.string = str(row['year'])
        municipality_tag.append(year_tag)
        total_tag = soup.new_tag("total")
        total_tag.string = str(row['total'])
        municipality_tag.append(total_tag)
        males_tag = soup.new_tag("males")
        males_tag.string = str(row['males'])
        municipality_tag.append(males_tag)
        females_tag = soup.new_tag("females")
        females_tag.string = str(row['females'])
        municipality_tag.append(females_tag)
        root.append(municipality_tag)

    # create file and write
    file = codecs.open(xml_file, "w", "utf-8")
    file.write(soup.prettify())
    file.close()


if __name__ == '__main__':
    read_csv_and_create_xml(str(sys.argv[1]), str(sys.argv[2]))
