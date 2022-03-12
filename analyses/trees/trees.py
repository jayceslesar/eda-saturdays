import os
import pandas as pd
import plotly.graph_objs as go

data_path = os.path.join('data', 'planting-sites.csv')
df = pd.read_csv(data_path)  # global read


def create_species(df):
    """Differentiate between species and subspecies."""
    df = df.rename(columns={'species': 'subspecies'})
    subspecies = df['subspecies']
    major_types = []
    new_subspecies = []
    for tree in subspecies:
        try:
            species_subspecies = tree.split(',')
            if len(species_subspecies) == 2:
                major_types.append(species_subspecies[0])
                new_subspecies.append(species_subspecies[1])
            else:
                major_types.append(tree)
                new_subspecies.append(tree)

        except AttributeError:
            major_types.append(float('nan'))
            new_subspecies.append(float('nan'))

    df['species'] = major_types
    df['subspecies'] = new_subspecies

    return df


df.drop('park', axis=1, inplace=True)  # bad column essentially, not all trees are in parks, can come back to this later
df = create_species(df)


def species_counts_plot(df):
    data = df['species'].value_counts()
    values = data.values
    names = data.index.tolist()
    fig = go.Figure([go.Bar(x=names, y=values)])
    fig.update_xaxes(title='Species')
    fig.update_yaxes(title='Count')
    fig.update_layout(title='Value Counts Bar Graph for Tree Types in Burlington, VT')
    fig.show()


def species_value(df):
    grouped = df.groupby('species')['appraise'].mean().to_frame()
    grouped['species'] = grouped.index
    grouped.reset_index(drop=True, inplace=True)
    sorted_groups = grouped.sort_values('appraise', ascending=False)
    fig = go.Figure([go.Bar(x=sorted_groups['species'], y=sorted_groups['appraise'])])
    fig.update_xaxes(title='Species', type='category', dtick=1)
    fig.update_yaxes(title='Mean Appraisal Value ($)')
    fig.update_layout(title='Mean Appraisal for Tree Types in Burlington, VT')
    fig.show()


def tree_counts_by_ward(df):
    ward_df = pd.DataFrame()
    wards = sorted(df['zone_id'].unique()[:-1])
    mean_ward_prices = []
    total_ward_prices = []
    ward_tree_counts = []

    for ward in wards:
        curr_ward_df = df[df['zone_id'] == ward]
        mean_ward_prices.append(curr_ward_df['appraise'].mean())
        total_ward_prices.append(curr_ward_df['appraise'].sum())
        ward_tree_counts.append(len(curr_ward_df))

    ward_df['ward'] = wards
    ward_df['mean_tree_value'] = mean_ward_prices
    ward_df['total_tree_value'] = total_ward_prices
    ward_df['tree_count'] = ward_tree_counts

    colors = ['green', 'goldenrod', 'blue', 'red', 'purple', 'maroon', 'orange', 'cyan']
    # mean value
    fig = go.Figure(go.Bar(x=ward_df['ward'], y=ward_df['mean_tree_value'], marker_color=colors))
    fig.update_xaxes(title='Ward')
    fig.update_yaxes(title='Mean Tree Value ($)')
    fig.update_layout(title='Mean Tree Value by Ward')
    fig.show()
    # total value
    fig = go.Figure(go.Bar(x=ward_df['ward'], y=ward_df['total_tree_value'], marker_color=colors))
    fig.update_xaxes(title='Ward')
    fig.update_yaxes(title='Total Tree Value ($)')
    fig.update_layout(title='Total Tree Value by Ward')
    fig.show()
    # # num trees
    fig = go.Figure(go.Bar(x=ward_df['ward'], y=ward_df['tree_count'], marker_color=colors))
    fig.update_xaxes(title='Ward')
    fig.update_yaxes(title='Tree Count')
    fig.update_layout(title='Total Trees by Ward')
    fig.show()


def tree_counts_by_land_use(df):
    land_df = pd.DataFrame()
    lands = [land for land in df['landuse'].unique() if isinstance(land, str)]
    mean_land_prices = []
    total_land_prices = []
    land_tree_counts = []

    for land in lands:
        curr_land_df = df[df['landuse'] == land]
        mean_land_prices.append(curr_land_df['appraise'].mean())
        total_land_prices.append(curr_land_df['appraise'].sum())
        land_tree_counts.append(len(curr_land_df))

    land_df['land'] = lands
    land_df['mean_tree_value'] = mean_land_prices
    land_df['total_tree_value'] = total_land_prices
    land_df['tree_count'] = land_tree_counts


    colors = ['mintcream', 'wheat', 'silver', 'green', 'goldenrod', 'blue', 'red', 'purple', 'maroon', 'orange', 'cyan', 'hotpink', 'darkkhaki', 'lavender']
    # mean value
    fig = go.Figure(go.Bar(x=land_df['land'], y=land_df['mean_tree_value'], marker_color=colors))
    fig.update_xaxes(title='Land Type')
    fig.update_yaxes(title='Mean Tree Value ($)')
    fig.update_layout(title='Mean Tree Value by Land Type')
    fig.show()
    # total value
    fig = go.Figure(go.Bar(x=land_df['land'], y=land_df['total_tree_value'], marker_color=colors))
    fig.update_xaxes(title='Land Type')
    fig.update_yaxes(title='Total Tree Value ($)')
    fig.update_layout(title='Total Tree Value by Land Type')
    fig.show()
    # # num trees
    fig = go.Figure(go.Bar(x=land_df['land'], y=land_df['tree_count'], marker_color=colors))
    fig.update_xaxes(title='Land Type')
    fig.update_yaxes(title='Tree Count')
    fig.update_layout(title='Total Trees by Land Type')
    fig.show()
