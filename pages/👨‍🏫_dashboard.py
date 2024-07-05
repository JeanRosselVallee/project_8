# Init
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath('./utils'))
import my_functions as my
my.print_debug('Version 0.0.2') 

str_author = 'Jean Vallée'
str_title = '👨‍🏫Dashboard'

st.title(str_title)                # STREAM: print Title

# Debug
current_dir = os.getcwd()
my.print_debug(f'PWD={current_dir}')

# Left SideBar
menu = st.sidebar
menu.title(str_title)
menu.info('Customer profile with main features')

# Load Features
path_csv = current_dir + '/data/in/X_simplified_4.csv'
df_X = my.load_data(path_csv, 10)

# Application Selection
#if 'selectbox_request_key' not in st.session_state : st.session_state.selectbox_request_key = 0
request_ref = df_X['ref'] #.drop_duplicates()
selectbox_request = st.sidebar.selectbox(
    "Credit Application", request_ref, index=0, key=5) #st.session_state.selectbox_request_key)

menu.image('https://img.freepik.com/vecteurs-premium/icone-score-indicateur-credit-indique-niveau-solvabilite_485380-2529.jpg')
menu.html(f'<hr> <p align="right">{str_author}</p>')

# Load Targets
path_csv = current_dir + '/data/in/y_train_2.csv'
df_y = my.load_data(path_csv, 10)

# Display Data
st.subheader('df_y')                # STREAM: print Title
st_text1 = st.text('Loading data...')      # STREAM: print Text
st.write(df_y)                  # STREAM: print Pandas
st_text1.text('Data loaded!')		

# Markdown
st.markdown(						# STREAM: MarkDown
    """
    **👈 Simple Streamlit app** to see some examples
    of what Streamlit can do!
    ### See more complex demos
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

# Condition
if st.checkbox('Show raw data'):			# STREAM: input Checkbox
	
# Table
	st.subheader('Raw data')				# STREAM: print Title
	st.write(data)						# STREAM: print Pandas

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
