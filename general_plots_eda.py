# -*- coding: utf-8 -*-
"""EQ_TS_EDA_01.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aXvr85lOi-54Cge52zhHrx9rcD7yAG5e

# Data Processing and EDA for Earthquake Timesries Forecating

# A] Data Preprocessing
"""

#!pip install plotly-express

import pandas as pd
import numpy as np
import datetime
from datetime import datetime 
import plotly.express as px
import streamlit as st

df=pd.read_csv("all_month.csv")

#df.shape

#df.info()

#df.head()

df['time'] = pd.to_datetime(df['time'])

df['date'] = pd.to_datetime(df['date'])

# extract year from date
df['month'] = pd.DatetimeIndex(df['time']).month_name()

#df['month']

# seperating 'place' column and only consider city by seperating the location by ', '
newdf = df['place'].str.split(', ', expand=True)
#newdf.head()

df['location'] = newdf[1]

#df['location']

"""# Checking for null values"""

#df.isnull().sum()

"""Found 1 empty value in mag and 379 empty values in place"""

#df.head()

#df.columns


# Soring records based on time
df = df.sort_values('date', ascending=True)

# setting date as the index column
df.set_index('date')

# Keeping only required columns
df = df[['date','time','latitude', 'longitude','location', 'depth', 'mag','type', 'month']]

#df.head()

# Creating a new dataset containing only earthquakes
eq_df = df.loc[df['type'] == 'earthquake',:]

#eq_df.head()
# B] Exploratory Data Analysis

# General Analysis
def view_data():
    st.subheader(" Dataset - ")
    st.write("Shown below is the dataset used for this work, obtained from the USGS Earthquake Hazard Program's Earthquake Catalog.")
    def color_vals(value):
        """
        Colors elements in a dateframe
        green if positive and red if
        negative. Does not color NaN
        values.
        """

        if value < 0:
            color = 'red'
        elif value > 0:
            color = 'green'
        else:
            color = 'white'

        return 'color: %s' % color
    view_df = df[:10]
    view_df = view_df.style.applymap(color_vals, subset=['mag', 'depth'])
    st.table(view_df)

def gen_analysis():

    # total events
    tot_eve = df['type'].shape[0]

    # tot eq events
    tot_eq_eve = df[df['type'] == 'earthquake'].shape[0]

    # min magnitude
    mag_min = df['mag'].min()

    # max magnitude
    mag_max = df['mag'].max()

    # min depth
    dep_min = round(df['depth'].min(),2)

    # max depth
    dep_max = df['depth'].max()

    col1, col2 = st.columns(2)
    col1.metric("Total Events", tot_eve)
    col2.metric("Total Earthquake Events", tot_eq_eve)

    col3,col4, col5, col6 = st.columns(4)
    col3.metric("Minimum Magnitude", mag_min)
    col4.metric("Maximum Magnitude", mag_max)
    col5.metric("Minimum Depth", dep_min)
    col6.metric("Maximum Depth", dep_max)





## 1. Creating a histogram to show number of events occured
def number_of_events_occured():
    fig1 = px.histogram(df, 'time', color="type", title="Number of Events", template="plotly_dark")
    st.plotly_chart(fig1)
    st.write("The above histogram represents the number of events that occured at a particular time.")

"""## 2. Creating a pie chart to display percentage of events per month """
def percentage_of_events_per_month():
    fig2 = px.pie(data_frame=df,
           names='month',
           title='Percentage of events w.r.t. month', template="plotly_dark")
    st.plotly_chart(fig2)
    st.write("The above Pie-Chart represents the percentage of events that took place per month.")
    st.write("It can be observed that the most number of events occured in the month of July.")

"""## 3. Creating a Pie Chart to to display the proportion of each type of events in the dataset"""
def proportion_of_events():
    fig3 = px.pie(data_frame=df,
           names='type',
           title='Proportion of events', template="plotly_dark")
    st.plotly_chart(fig3)
    st.write("The above Pie-Chart represents the proportion of various types of events present in the dataset.")
    st.write("It can be observed that the most number of events belong to the type Earthquake.")

"""## 4. Creating a histogram to show number of earthquake events occured """
def number_of_earthquake_events():
    fig4 = px.histogram(eq_df, 'time', color="type", title="Number of Earthquakes Events", template="plotly_dark")
    st.plotly_chart(fig4)
    st.write("The above histogram represents the number of earthquake events that occured at a particular time.")


"""## 5. Creating a histogram to display magnitude repartitions"""
def magnitude_repartitions():
    fig5 = px.histogram(eq_df, x = 'mag', nbins=50,title='Earthquake Magnitude Repartition', template="plotly_dark")
    st.plotly_chart(fig5)
    st.write("The above histogram represents the earthquake magnitude repartitions.")
    st.write("Higher the Magnitude, Lower the count of observations.")

## 6. Creating a histogram to display depth repartitions
def  depth_repartitions():
    fig6 = px.histogram(eq_df, x = 'depth', nbins=50,title='Earthquake Depth Repartition', template="plotly_dark")
    st.plotly_chart(fig6)
    st.write("The above histogram represents the earthquake depth repartitions.")
    st.write("Higher the Depth, Lower the count of observations.")

# 7. Creating a table to display places with highest magnitudes
def places_with_highest_mags():
    st.subheader("Top 3 Places with Highest Magnitude")
    # top 3 places with highest magnitude
    max_mag_places_df = eq_df.sort_values('mag', ascending=False)
    max_mag_places_df = max_mag_places_df[['location', 'mag']]
    blankIndex = [''] * len(
        max_mag_places_df)  # https://stackoverflow.com/questions/24644656/how-to-print-pandas-dataframe-without-index
    max_mag_places_df.index = blankIndex
    max_mag_places_df = max_mag_places_df[:3]
    st.table(max_mag_places_df)
    st.write("The above table displays the top 3 locations having the highest magnitudes.")
    st.write("Alaska appears to be the most dangerous place with an earthquake magnitude of 7.8.")

# 8. Creating a table to display places with highest depths
def places_with_highest_depths():
    # viewing top 3 places with highest depth
    st.subheader("Top 3 Places with Highest Depth")
    # top 3 places with highest magnitude
    max_dep_places_df = eq_df.sort_values('depth', ascending=False)
    max_dep_places_df = max_dep_places_df[['location', 'depth']]
    blankIndex = [''] * len(
        max_dep_places_df)  # https://stackoverflow.com/questions/24644656/how-to-print-pandas-dataframe-without-index
    max_dep_places_df.index = blankIndex
    max_dep_places_df = max_dep_places_df[:3]
    st.table(max_dep_places_df)
    st.write("The above table displays the top 3 locations having the highest depths.")
    st.write("Fiji appears to be the most dangerous place with an earthquake depth of 636.08m.")


# 9. Distribution of earthquakes w.r.t. to magnitude
def eq_distr_w_r_t_magnitude():
    # https://plotly.com/python/mapbox-layers/
    fig9 = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="mag", zoom=0.5,
                            mapbox_style="stamen-watercolor", color_continuous_scale='Thermal', range_color=[0.0, 8.0],
                            template="plotly_dark"
                            )

    st.plotly_chart(fig9)
    st.write("The above map displays the distribution of earthquakes across the globe with respect to magnitude.")
    st.write("The color scale changes from blue towards yellow as the magnitude progresses from 0 to the maximum value.")

# 10. Distribution of earthquakes w.r.t. depth
def eq_distr_w_r_t_depth():

    # https://plotly.com/python/mapbox-layers/
    fig10 = px.scatter_mapbox(df, lat="latitude", lon="longitude", color="depth", zoom=0.5,
                            mapbox_style="stamen-watercolor", color_continuous_scale='Thermal', range_color=[0.0, 8.0],
                            template="plotly_dark"
                            )

    st.plotly_chart(fig10)
    st.write("The above map displays the distribution of earthquakes across the globe with respect to depth.")
    st.write("The color scale changes from blue towards yellow as the depth progresses from 0 to the maximum value.")


# 11. Display scatter plot to show distribution of magnitude over the time
def eq_mag_scatter():
  fig11 = px.scatter(eq_df, x="date", y="mag",hover_name="location",hover_data=["location"], color="mag", template="plotly_dark")
  st.plotly_chart(fig11)
  st.write("The above scatter plot shows the distribution of magnitudes over the time.")


# 12. Display scatter plot to show distribution of depth over the time
def eq_depth_scatter():
  fig12 = px.scatter(eq_df, x="date", y="depth",hover_name="location",hover_data=["location"], color="depth", template="plotly_dark")
  st.plotly_chart(fig12)
  st.write("The above scatter plot shows the distribution of depths over the time.")
