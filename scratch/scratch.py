import matplotlib.pyplot as plt
import pandas as pd

hs = pd.read_html("https://en.wikipedia.org/wiki/World_Happiness_Report")
hs = hs.pop(0)
hs.drop(hs.columns[[0, 1, 4, 5, 6, 7, 8, 9, 10, 11]], axis=1, inplace=True)
hs = hs.iloc[1:]
hs.set_index(2, inplace=True)
hs.rename(columns={3: 'test'}, inplace=True)

print(hs)
print(type(hs))
print(hs['test'])
print(type(hs['test']))
print(hs['test'].max())

