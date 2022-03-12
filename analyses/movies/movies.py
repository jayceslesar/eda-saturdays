import os
import pandas as pd
import plotly.graph_objs as go

data_path = os.path.join('data', 'imdb_data.csv')
df = pd.read_csv(data_path)  # global read
for col in df.columns:
    print(f"{col}: {df.iloc[0][col]}, {type(df.iloc[0][col])}")


"""
Things to analyze

Actor frequency distribution
Director frequency distribution
Story frequency distribution
Total Movies/year
Popularity distribution
Runtime distribution
Average rating/director
Average rating/actor
Average popularity/director
Most common genre per director
Most common genre per actor
"""
