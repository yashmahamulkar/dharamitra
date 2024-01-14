import pandas as pd

df = pd.read_csv('clean.csv',encoding = "ISO-8859-1")

new_df = df.dropna()

print(new_df.to_string())
