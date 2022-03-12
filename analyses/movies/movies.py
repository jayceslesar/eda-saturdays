import os
import pandas as pd
import plotly.graph_objs as go

data_path = os.path.join('data', 'imdb_data.csv')
df = pd.read_csv(data_path)  # global read
