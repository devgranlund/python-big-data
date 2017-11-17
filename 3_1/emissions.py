import pandas as pd

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

df = df.dropna(subset=['ensirekisterointipvm'])
df = df.dropna(subset=['Co2'])
f = lambda x: x[:4]
df['ensirekisterointipvm'] = df['ensirekisterointipvm'].map(f)

print(df)
