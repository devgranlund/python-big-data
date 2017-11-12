import pandas as pd
import matplotlib.pyplot as plt

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

# Count the most popular cars
kaikki_lkm = len(df.index)
merkit = df.merkkiSelvakielinen.value_counts()
first_car = merkit.index[0]
first_car_count = merkit.get(first_car)
first_car_pr = (first_car_count/kaikki_lkm) * 100
second_car = merkit.index[1]
second_car_count = merkit.get(second_car)
second_car_pr = (second_car_count/kaikki_lkm) * 100
third_car = merkit.index[2]
third_car_count = merkit.get(third_car)
third_car_pr = (third_car_count/kaikki_lkm) * 100
fourth_car = merkit.index[3]
fourth_car_count = merkit.get(fourth_car)
fourth_car_pr = (fourth_car_count/kaikki_lkm) * 100
fifth_car = merkit.index[4]
fifth_car_count = merkit.get(fifth_car)
fifth_car_pr = (fifth_car_count/kaikki_lkm) * 100
others = 'Others'
others_count = kaikki_lkm - first_car_count - second_car_count - third_car_count - fourth_car_count - fifth_car_count
others_pr = (others_count/kaikki_lkm) * 100

labels = [first_car, second_car, third_car, fourth_car, fifth_car, others]
sizes = [first_car_pr, second_car_pr, third_car_pr, fourth_car_pr, fifth_car_pr, others_pr]
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax1.axis('equal')

# The shares of cars by travel distance
first_cat = '0-50000 km'
first_cat_count = len(df[(df['matkamittarilukema'] <= 50000)].index)
first_cat_pr = (first_cat_count/kaikki_lkm) * 100
second_cat = '50001-100000 km'
second_cat_count = len(df[(df['matkamittarilukema'].between(50001, 100000))].index)
second_cat_pr = (second_cat_count/kaikki_lkm) * 100
third_cat = '100001-150000 km'
third_cat_count = len(df[(df['matkamittarilukema'].between(100001, 150000))].index)
third_cat_pr = (third_cat_count/kaikki_lkm) * 100
fourth_cat = '150001-200000 km'
fourth_cat_count = len(df[(df['matkamittarilukema'].between(150001, 200000))].index)
fourth_cat_pr = (fourth_cat_count/kaikki_lkm) * 100
fifth_cat = '200001-250000 km'
fifth_cat_count = len(df[(df['matkamittarilukema'].between(200001, 250000))].index)
fifth_cat_pr = (fifth_cat_count/kaikki_lkm) * 100
sixth_cat = '250001-300000 km'
sixth_cat_count = len(df[(df['matkamittarilukema'].between(250001, 300000))].index)
sixth_cat_pr = (sixth_cat_count/kaikki_lkm) * 100
seventh_cat = 'over 300000 km'
seventh_cat_count = len(df[(df['matkamittarilukema'] > 300000)].index)
seventh_cat_pr = (sixth_cat_count/kaikki_lkm) * 100

labels = [first_cat, second_cat, third_cat, fourth_cat, fifth_cat, sixth_cat, seventh_cat]
sizes = [first_cat_pr, second_cat_pr, third_cat_pr, fourth_cat_pr, fifth_cat_pr, sixth_cat_pr, seventh_cat_pr]
fig2, ax2 = plt.subplots()
ax2.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax2.axis('equal')

plt.show()

# veh_data = veh_data.loc[veh_data['ajoneuvoluokka'].isin('M1', 'M1G')]

# print(merkki_selvakielinen)

