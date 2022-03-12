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

Done :)
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

Done :)
Conditional Frequencies
Most common genre per director
Most common genre per actor

Networks!
"""


def counts(df, column):
    """Takes df and variable with list vals and flattens to counts dictionary.
    """
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


def conditional(df, column, cutoff):
    count = counts(df, column)
    keys = [key for key in count if count[key] > cutoff]
    to_plot = {}
    for key in keys:
        if column == 'actors':
            movies = df[df[column].str.contains(key)]
        else:
            movies = df[df[column] == key]
        genre_counts = counts(movies, 'genre')
        highest_genre_key = list(genre_counts.keys())[-1]
        to_plot[f'{key} - {highest_genre_key}'] = genre_counts[highest_genre_key]

    sorted_to_plot = dict(sorted(to_plot.items(), key=lambda item: item[1]))
    x = []
    y = []
    for key in sorted_to_plot:
        x.append(key)
        y.append(sorted_to_plot[key])

    return x, y


def most_common_genre_plots(df):
    cutoff = 25
    x, y = conditional(df, 'directors', cutoff)
    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.update_layout(title=f'Movie Genre Count for Most Common Genre for a Director who Directed > {cutoff} Movies')
    fig.update_xaxes(title='Director - Most Common Genre')
    fig.update_yaxes(title='Count')
    fig.show()

    cutoff = 50
    x, y = conditional(df, 'actors', cutoff)
    fig = go.Figure([go.Bar(x=x, y=y)])
    fig.update_layout(title=f'Movie Genre Count for Most Common Genre for an Actor Who Acted in > {cutoff} Movies')
    fig.update_xaxes(title='Actor - Most Common Genre')
    fig.update_yaxes(title='Count')
    fig.show()


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
