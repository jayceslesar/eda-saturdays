import os
import numpy as np
import pandas as pd
import plotly.graph_objs as go

data_path = os.path.join('data', 'imdb_data.csv')
df = pd.read_csv(data_path)  # global read
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


def counts(df, column):
    to_flatten = df[column].values
    counts = {}
    for things in to_flatten:
        if ',' in things:
            splits = things.split(',')
        else:
            splits = [things]

        for thing in splits:
            if thing in counts:
                counts[thing] += 1
            else:
                counts[thing] = 1

    return dict(sorted(counts.items(), key=lambda item: item[1]))


def plot_counts(df, column):
    count = counts(df, column)
    values = list(count.values())
    distinct_vals = set(values)
    x = []
    y = []
    for val in distinct_vals:
        x.append(val)
        y.append(values.count(val))

    fig = go.Figure(go.Scatter(x=np.log10(x), y=np.log10(y), mode='markers'))
    return fig


def n_sub_k_plots(df):
    director_fig = plot_counts(df, 'directors')
    director_fig.update_xaxes(title='Log 10 Number of Movies Directed')
    director_fig.update_yaxes(title='Log 10 Number of Directors Who Have Directed That Number of Movies')
    director_fig.update_layout(title='Zipf Law of Directed Movie Counts for Directors')
    director_fig.show()

    actors_fig = plot_counts(df, 'actors')
    actors_fig.update_xaxes(title='Log 10 Number of Movies Acted in')
    actors_fig.update_yaxes(title='Log 10 Number of Actors Who Have Acted in That Number of Movies')
    actors_fig.update_layout(title='Zipf Law of Acted Movie Counts for Actors')
    actors_fig.show()

    story_fig = plot_counts(df, 'story')
    story_fig.update_xaxes(title='Log 10 Number of Story')
    story_fig.update_yaxes(title='Log 10 Number of Story That Appear Some Number of Times')
    story_fig.update_layout(title='Zipf Law of Story Counts')
    story_fig.show()

