# IMDB Analysis
Data from kaggle [here](https://www.kaggle.com/hyeonwooan/imdb-data-preprocessed-using-ml20m/version/2?select=imdb_data.csv).


| Variable | Data Type | Converted Data Type |
| -----------| -------- | -------- |
| id | string |  |
| name | string | |
| year | string | integer |
| grade | string | |
| runtime | string | integer |
| directors | string | |
| actors | string | |
| genre | string | |
| rating | string | |
| votes | string | |
| story | string | |
| actors_order | string | |
| directors_order | string | |
| popularity | float | |
# Data Cleaning
Year variable is pretty bad, needed a good amount of data cleaning brought to you by the function `clean_integer`.

On closer inspection we can see that the actors and directors columns often have multiple of each, not not all. This is ripe for a network



# Analysis
For the analysis, I came up with a few general questions I could use this dataset to investigate, all related to tree distribution and value of different types of land by trees.  All data cleaning and graphing done in pandas and plotly respectively.

## Species counts
![species counts](images/species_bar.png)
Here we can see a clear power law for species counts of trees. I am no tree expert but can definitely assume that tree type distributions are not often uniform, especially in areas where people have control over what grows where.

## Do different species have different values?
![species counts](images/species_price.png)
Looking at mean price per tree, we can see that some trees are appraised at a much higher value than others. The smoketree comes in at a whopping 25k with the majority of other trees falling below 5k USD in appraisal value.

## Ward value in terms of trees in that ward
Let's see if we can find some inequalities between wards. Not every ward is likely created equal (some may be more industrial and others may be more residential) so we cannot assume that they should look uniform.

| Mean Ward Value in Tree Appraisal | Total Ward Value in Tree Appraisal | Total Tree Count in Ward |
| ------------------------- | ------------------------- | ------------------------- |
|![mean ward tree value](images/mean_ward_value.png) | ![total ward tree value](images/total_ward_value.png) | ![total ward tree count](images/num_trees_ward.png)|

## Land type value in terms of trees in that type of land
Similarly, we can do the same for land use types.
| Mean Land Type Value in Tree Appraisal | Total Land Type Value in Tree Appraisal | Total Tree Count in Land Type |
| ------------------------- | ------------------------- | ------------------------- |
|![mean land tree value](images/mean_land_value.png) | ![total land tree value](images/total_land_value.png) | ![total land tree count](images/num_trees_land.png)|
