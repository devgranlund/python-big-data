import pandas as pd
import matplotlib.pyplot as plt
import datetime
from matplotlib.gridspec import GridSpec

# Author: tuomas.granlund@solita.fi
# 12.11.2017

# Data must be read by iterating chunks for memory reasons
reader = pd.read_csv('tieliikenne_data.csv', delimiter=';', encoding='latin_1', iterator=True)
chunks = []
loop = True
while loop:
    try:
        chunk = reader.get_chunk(1000)[['ajoneuvoluokka', 'merkkiSelvakielinen',
                                        'matkamittarilukema', 'ensirekisterointipvm', 'Co2']]
        filtered = chunk[(chunk['ajoneuvoluokka'].isin(['M1', 'M1G']))]
        chunks.append(filtered)
    except StopIteration:
        loop = False

df = pd.concat(chunks, ignore_index=True)

# The most popular cars
count_of_all_cars = len(df.index)
car_brands = df.merkkiSelvakielinen.value_counts()
car_1 = car_brands.index[0]
car_1_count = car_brands.get(car_1)
car_1_pr = (car_1_count / count_of_all_cars) * 100
car_2 = car_brands.index[1]
car_2_count = car_brands.get(car_2)
car_2_pr = (car_2_count / count_of_all_cars) * 100
car_3 = car_brands.index[2]
car_3_count = car_brands.get(car_3)
car_3_pr = (car_3_count / count_of_all_cars) * 100
car_4 = car_brands.index[3]
car_4_count = car_brands.get(car_4)
car_4_pr = (car_4_count / count_of_all_cars) * 100
car_5 = car_brands.index[4]
car_5_count = car_brands.get(car_5)
car_5_pr = (car_5_count / count_of_all_cars) * 100
others = 'Others'
others_count = count_of_all_cars - car_1_count - car_2_count - car_3_count - car_4_count - car_5_count
others_pr = (others_count / count_of_all_cars) * 100

labels = [car_1, car_2, car_3, car_4, car_5, others]
sizes = [car_1_pr, car_2_pr, car_3_pr, car_4_pr, car_5_pr, others_pr]

the_grid = GridSpec(2, 2)
plt.subplot(the_grid[0, 0], aspect=1)
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.axis('equal')

# The shares of cars by travel distance
cat_1 = '0-50000 km'
cat_1_count = len(df[(df['matkamittarilukema'] <= 50000)].index)
cat_1_pr = (cat_1_count / count_of_all_cars) * 100
cat_2 = '50001-100000 km'
cat_2_count = len(df[(df['matkamittarilukema'].between(50001, 100000))].index)
cat_2_pr = (cat_2_count / count_of_all_cars) * 100
cat_3 = '100001-150000 km'
cat_3_count = len(df[(df['matkamittarilukema'].between(100001, 150000))].index)
cat_3_pr = (cat_3_count / count_of_all_cars) * 100
cat_4 = '150001-200000 km'
cat_4_count = len(df[(df['matkamittarilukema'].between(150001, 200000))].index)
cat_4_pr = (cat_4_count / count_of_all_cars) * 100
cat_5 = '200001-250000 km'
cat_5_count = len(df[(df['matkamittarilukema'].between(200001, 250000))].index)
cat_5_pr = (cat_5_count / count_of_all_cars) * 100
cat_6 = '250001-300000 km'
cat_6_count = len(df[(df['matkamittarilukema'].between(250001, 300000))].index)
cat_6_pr = (cat_6_count / count_of_all_cars) * 100
cat_7 = 'over 300000 km'
cat_7_count = len(df[(df['matkamittarilukema'] > 300000)].index)
cat_7_pr = (cat_6_count / count_of_all_cars) * 100

labels = [cat_1, cat_2, cat_3, cat_4, cat_5, cat_6, cat_7]
sizes = [cat_1_pr, cat_2_pr, cat_3_pr, cat_4_pr, cat_5_pr, cat_6_pr, cat_7_pr]
plt.subplot(the_grid[0, 1], aspect=1)
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.axis('equal')

# How old are the cars?
df['ensirekisterointipvm'] = pd.to_datetime(df['ensirekisterointipvm'], format="%Y-%m-%d")
now = datetime.datetime.utcnow()
f = lambda x: (now - x).days / 360
s_old_count = len(df[(df['ensirekisterointipvm'].map(f) <= 5)].index)
s_old_count_pr = (s_old_count / count_of_all_cars) * 100
m_old_count = len(df[(df['ensirekisterointipvm'].map(f).between(5.000001, 10))].index)
m_old_count_pr = (m_old_count / count_of_all_cars) * 100
l_old_count = len(df[(df['ensirekisterointipvm'].map(f).between(10.000001, 15))].index)
l_old_count_pr = (l_old_count / count_of_all_cars) * 100
xl_old_count = len(df[(df['ensirekisterointipvm'].map(f).between(15.000001, 20))].index)
xl_old_count_pr = (xl_old_count / count_of_all_cars) * 100
xxl_old_count = len(df[(df['ensirekisterointipvm'].map(f) > 20)].index)
xxl_old_count_pr = (xxl_old_count / count_of_all_cars) * 100

labels = ['under 5 y old', '5 - 10 y old', '10 - 15 y old',
          '15 - 20 y old', 'over 20 y old']
sizes = [s_old_count_pr, m_old_count_pr, l_old_count_pr, xl_old_count_pr, xxl_old_count_pr]
plt.subplot(the_grid[1, 0], aspect=1)
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.axis('equal')

# CO2 emissions
co_1 = len(df[(df['Co2'] <= 100)].index)
co_1_pr = (co_1 / count_of_all_cars) * 100
co_2 = len(df[(df['Co2'].between(101, 125))].index)
co_2_pr = (co_2 / count_of_all_cars) * 100
co_3 = len(df[(df['Co2'].between(126, 150))].index)
co_3_pr = (co_3 / count_of_all_cars) * 100
co_4 = len(df[(df['Co2'].between(151, 175))].index)
co_4_pr = (co_4 / count_of_all_cars) * 100
co_5 = len(df[(df['Co2'].between(176, 200))].index)
co_5_pr = (co_5 / count_of_all_cars) * 100
co_6 = len(df[(df['Co2'].between(201, 225))].index)
co_6_pr = (co_6 / count_of_all_cars) * 100
co_7 = len(df[(df['Co2'].between(226, 250))].index)
co_7_pr = (co_7 / count_of_all_cars) * 100
co_8 = len(df[(df['Co2'] > 250)].index)
co_8_pr = (co_8 / count_of_all_cars) * 100

labels = ['under 100 g/km', '100 - 125 g/km', '125 - 150 g/km', '150 - 175 g/km', '175 - 200 g/km',
          '200 - 225 g/km', '225 - 250 g/km', 'over 250 g/km']
sizes = [co_1_pr, co_2_pr, co_3_pr, co_4_pr, co_5_pr, co_6_pr, co_7_pr, co_8_pr]
plt.subplot(the_grid[1, 1])
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
plt.axis('equal')

# Create the picture
plt.subplots_adjust(top=0.98, bottom=0.02)
plt.tight_layout()
plt.savefig('vehstats.png')

# veh_data = veh_data.loc[veh_data['ajoneuvoluokka'].isin('M1', 'M1G')]

# print(merkki_selvakielinen)

# def count_years(now, )
