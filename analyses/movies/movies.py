from locale import D_FMT
import os
import numpy as np
import pandas as pd
import plotly.graph_objs as go


def clean_numeric(df, col_name):
    """Converts year from string with parentheses to integer year value.
    """
    vals = []
    for val in df[col_name].values:

        if not pd.isna(val):
            digits = ""
            for c in val:
                if c.isdigit():
                    digits += c

            if digits == "":
                vals.append(-1)
            else:
                vals.append(int(digits))
        else:
            vals.append(val)

    df[col_name] = np.asarray(vals)


def clean_runtime(df):
    """Converts runtime from string expression in minutes to integer year in minutes.
    """
    df["runtime"] = [int(runtime.rstrip(" min")) if not pd.isna(runtime) and runtime !="None" else runtime for runtime in df["runtime"].values]


data_path = os.path.join('data', 'imdb_data.csv')
df = pd.read_csv(data_path)  # global read

# Data Cleaning
clean_numeric(df, "year")
clean_numeric(df, "runtime")

for col in df.columns:
    print(f"{col}: {df.iloc[0][col]}, {type(df.iloc[0][col])}")

"""
Things to analyze

Frequency Distributions
Actor frequency distribution
Director frequency distribution
Story frequency distribution

Numeric Distributions
Popularity distribution
Runtime distribution

Numeric Distributions in Time

Numeric Distributions by Categories
Average rating/director
Average rating/actor
Average rating/genre
Average popularity/director

Conditional Frequencies
Most common genre per director
Most common genre per actor

Networks!
"""


def frequency(df, column):
    """Takes df and variable with list vals and flattens to counts dictionary.
    """
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
