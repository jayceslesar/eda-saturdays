import os
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.figure_factory as ff
import networkx as nx
import plotly.express as px
from collections import Counter

FIRST_MOVIE_YEAR = 1878
THIS_YEAR = 2022

"""DATA CLEANING
"""
def clean_integer(df, col_name):
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


def clean_float(df, col_name):
    """Converts year from string with parentheses to integer year value.
    """
    df[col_name] = [float(val) if val != "None" else None for val in df[col_name].values]


def clean_runtime(df):
    """Converts runtime from string expression in minutes to integer year in minutes.
    """
    df["runtime"] = [int(runtime.rstrip(" min")) if not pd.isna(runtime) and runtime !="None" else runtime for runtime in df["runtime"].values]


data_path = os.path.join('data', 'imdb_data.csv')
df = pd.read_csv(data_path)  # global read

# Data Cleaning
int_cols = ["year",  "runtime", "votes"]
float_cols = ["rating", "popularity"]

for col in float_cols:
    clean_float(df, col)
for col in int_cols:
    clean_integer(df, col)

# for col in df.columns:
#     print(f"{col}: {df.iloc[0][col]}, {type(df.iloc[0][col])}")


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


def dist_by_rating(df):
    hist_data = []
    names = []
    dont_use = ['Unrated', '7', 'Passed', 'Approved', '12', 'GP', '19', 'TV-14', 'TV-PG', 'None', 'Not Rated', 'Limited', '15', 'All']
    grouped = df.groupby(['grade'])
    for group, data in grouped:
        if group in dont_use:
            continue
        names.append(group)
        hist_data.append(data['popularity'].values)

    fig = ff.create_distplot(hist_data, names, curve_type='normal', bin_size=.05, show_hist=False)
    fig.show()


def connectivity(df, colname, year):
    d = {}
    df = df.dropna()
    df = df[df['year'].astype(int) == year]
    pers_counts = counts(df, colname)

    for index, row in df.iterrows():
        persons = row[colname].split(',')
        enough = []
        for pers in persons:
            if pers_counts[pers] > 0:
                enough.append(pers)
        if enough:
            d[row['name']] = enough

    G = nx.DiGraph(d)
    conn_dict = nx.average_degree_connectivity(G)
    mean_conn = np.mean([value for value in conn_dict.values()])

    return mean_conn


def plot_connectivity(df):
    actors_conn = []
    directors_conn = []
    years = list(range(FIRST_MOVIE_YEAR, THIS_YEAR))
    for year in years:
        actors_conn.append(connectivity(df, 'actors', year))
        directors_conn.append(connectivity(df, 'directors', year))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=actors_conn, mode='markers', name='Actor Connectivity'))
    fig.add_trace(go.Scatter(x=years, y=directors_conn, mode='markers', name='Director Connectivity'))
    fig.update_layout(title=f'Average Connectivity by Year for Movies')
    fig.update_xaxes(title='Year')
    fig.update_yaxes(title='Average Connectivity')
    fig.show()


# TODO: add optional categorical
def plot_mean_time(df, num_col:str):
    sorted_df = df.sort_values(by=["year"], ascending=True)[["year", num_col]]
    clean_df = sorted_df[(sorted_df['year'] > FIRST_MOVIE_YEAR) & (sorted_df['year'] <= THIS_YEAR)].dropna(subset=['year', num_col])
    clean_df['year'] = clean_df['year'].astype(str)

    year_counts = counts(clean_df, "year")
    counts_df = pd.DataFrame.from_dict(year_counts, orient='index')
    counts_df = counts_df.sort_index(ascending=True)

    year_means = clean_df.groupby(['year']).mean()
    year_means["counts"] = counts_df[0].values

    fig1 = px.scatter(year_means, x=year_means.index, y=num_col, color="counts", size = "counts", color_continuous_scale="blackbody")
    fig2 = px.line(year_means, x=year_means.index, y=num_col)
    fig3 = go.Figure(data=fig1.data + fig2.data, layout=fig1.layout)
    fig3.update_xaxes(title='Year')
    fig3.update_yaxes(title='Average Rating')
    fig3.update_layout(title='Average Movie Ratings over Time', width=1100, height=700)
    fig3.write_image("analyses/movies/images/"+num_col+".png")


def plot_col_dist(df, col, title):
    fig = px.histogram(df, x=col, marginal="box")
    fig.update_layout(title=title, width=1100, height=700)
    fig.write_image("analyses/movies/images/"+col+"_hist"+".png")


def plot_genre_counts(df):
    genres = ",".join(df["genre"].values).split(",")
    genre_counts = Counter(genres)
    genre_df = pd.DataFrame.from_dict(genre_counts, orient="index")

    fig = px.bar(genre_df, x=genre_df.index, y=[0], color=genre_df.index)
    fig.update_layout(showlegend=False)
    fig.update_xaxes(title='Genre')
    fig.update_yaxes(title='Count')
    fig.update_layout(title='Number of Movies per Genre', width=1100, height=700)
    fig.write_image("analyses/movies/images/"+"ratings_barplot"+".png")
plot_genre_counts(df)
plot_col_dist(df, "rating", "Movie Rating Distribution")
plot_mean_time(df, "rating")