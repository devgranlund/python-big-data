import pandas as pd
import numpy as np

# Author: TGr
# 17.11.2017

# Data must be read by iterating chunks for memory reasons
reader = pd.read_csv('tieliikenne_data.csv', delimiter=';', encoding='latin_1', iterator=True)
chunks = []
loop = True
while loop:
    try:
        chunk = reader.get_chunk(1000)[['ajoneuvoluokka', 'ensirekisterointipvm', 'Co2']]
        filtered = chunk[(chunk['ajoneuvoluokka'].isin(['M1', 'M1G']))]
        chunks.append(filtered)
    except StopIteration:
        loop = False

df = pd.concat(chunks, ignore_index=True)

# drop rows where ensirekisterointipvm is NaN
df = df.dropna(subset=['ensirekisterointipvm'])

# drop rows where Co2 is Nan
df = df.dropna(subset=['Co2'])

# convert date to year
f = lambda x: x[:4]
df['ensirekisterointipvm'] = df['ensirekisterointipvm'].map(f)

# pivot table
pivot = pd.pivot_table(df, index='ensirekisterointipvm', values=['Co2'], aggfunc=[np.average, len])

print(pivot)
