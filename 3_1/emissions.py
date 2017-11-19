import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Author: TGr
# 17.11.2017

luokka = 'ajoneuvoluokka'
pvm = 'ensirekisterointipvm'
co2 = 'Co2'

# Data must be read by iterating chunks for memory reasons
reader = pd.read_csv('tieliikenne_data.csv', delimiter=';', encoding='latin_1', iterator=True)
chunks = []
loop = True
while loop:
    try:
        chunk = reader.get_chunk(1000)[[luokka, pvm, co2]]
        filtered = chunk[(chunk[luokka].isin(['M1', 'M1G']))]
        chunks.append(filtered)
        loop = False # TODO remove this line from ready implementation
    except StopIteration:
        loop = False

df = pd.concat(chunks, ignore_index=True)

# drop rows where ensirekisterointipvm is NaN
df = df.dropna(subset=[pvm])

# drop rows where Co2 is Nan
df = df.dropna(subset=[co2])

# convert date to year
f = lambda x: x[:4]
df[pvm] = df[pvm].map(f)

# additional years
additional_years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', '2026', '2027', '2028', '2029', '2030']
labels = [pvm]
additional_years_df = pd.DataFrame(additional_years, columns=labels)
df = df.append(additional_years_df)

# pivot table
pivot = pd.pivot_table(df, index=pvm, values=[co2], aggfunc=[np.average, len])
print(pivot)
print(pivot.index)

# create figure
plt.figure(1, figsize=(10, 10))
plt.subplot()
plt.scatter(pivot.index, pivot.average[co2], s=2)
plt.xlabel(pvm)
plt.ylabel(co2)

plt.show()
