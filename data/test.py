import pandas as pd

df = pd.read_parquet("./raw/raw_data.parquet")

print(df.head())
