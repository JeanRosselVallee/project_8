# Import Modules
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import plotly.graph_objects as go

sys.path.insert(0, os.path.abspath('./utils'))
import my_functions as my		# Custom module	

Notes = '''
Current dir is project root's
'''

str_title = '👨‍🏫Dashboard'		# MetaData
my.debug(str_title + ' - Version 0.0.2') 
#st.title(str_title)             # STREAM: print Title
str_author = 'Jean Vallée'

# Data
## Features
path_X = './data/in/X_simplified_4.csv'
df_X = my.load_data(path_X, 10)	# Load
## Target
path_y = './data/in/y_train_2.csv'
df_y = my.load_data(path_y, 10)
df_y.columns = ['ref', 'class']
## Join
df_data = df_X.join(df_y, rsuffix='_todel')
df_data.columns = ['ref', 'male', 'score_A', 'score_B', 'edu_level_2', 'edu_level_3', 'cash_loan', 'employee', 'request_id', 'class']
df_data = df_data.drop('ref', axis='columns')
df_data.set_index('request_id', inplace=True)

# Left SideBar
menu = st.sidebar
menu.title(str_title)
menu.info('Customer profile with main features')

# Application Selection
#if 'selectbox_request_key' not in st.session_state : st.session_state.selectbox_request_key = 0
ser_request_ids = df_data.index
selected_ref = st.sidebar.selectbox('Credit Application', ser_request_ids, index=0) #st.session_state.selectbox_request_key)

# Table of 2 columns
frame_left, frame_right = st.columns([6, 4])

# Display Selected Record
selected_record = df_data.loc[[selected_ref]] 
frame_left.dataframe(selected_record)#[li_features]) 	

# Display Score Gauge
frame_right.plotly_chart(my.plot_gauge(75), use_container_width=True)

# Display All Targets
bool_show_targets = st.checkbox('Show all targets')	# STREAM: input Checkbox
if bool_show_targets :
	st.subheader('df_y')            # STREAM: print Title
	st.dataframe(df_y, hide_index=True)              # STREAM: print Pandas
	
menu.image('https://img.freepik.com/vecteurs-premium/icone-score-indicateur-credit-indique-niveau-solvabilite_485380-2529.jpg')
menu.html(f'<hr> <p align="right">{str_author}</p>')



# Markdown
st.markdown(						# STREAM: MarkDown
    """
    **👈 Simple Streamlit app** to see some examples
    of what Streamlit can do!
    ### See more complex demos
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

'''
# Histogram
st.subheader('Number of pickups by hour')	
hist_values = np.histogram(					# Create Histogram
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0] 
st.bar_chart(hist_values)					# STREAM: plot Graph

# Slicer
hour_to_filter = st.slider('hour', 0, 23, 17)  # (min, max, default)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# Map
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)						# STREAM: plot Map
'''



# Main
'''
st.title('simple_app')
number = st.slider("Pick a number", 0, 100)
st.write(f"You selected: {number}")
'''
