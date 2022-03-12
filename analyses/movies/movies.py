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
Average rating/genre
Average popularity/director
Most common genre per director
Most common genre per actor
"""


def frequency(df, column):
    to_flatten = df[column].values
    frequency = {}
    for things in to_flatten:
        if ',' in things:
            splits = things.split(',')
        else:
            splits = [things]

        for thing in splits:
            if thing in frequency:
                frequency[thing] += 1
            else:
                frequency[thing] = 1

    return frequency
