# Import Modules
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import plotly.graph_objects as go
import subprocess
import json

sys.path.insert(0, os.path.abspath('./utils'))
import my_functions as my		         # Custom module	

Notes = '''
Current dir is project root's
'''
str_logo = '👨‍🏫'
str_title = str_logo + 'Dashboard'	     # MetaData
my.debug(str_title + ' - Version 0.0.2') 
#st.title(str_title) # STREAM: print Title
str_author = 'Jean Vallée'

# Data
## Load
dir_in = './data/in/'
path_data = dir_in + 'data.csv'
df_data   = my.load_data(path_data, 10)	
df_data.set_index('request_id', inplace=True)

# Left SideBar
menu = st.sidebar
menu.title(str_title)
menu.info('Customer profile with main features')

# Application Selection
#if 'selectbox_request_key' not in st.session_state : st.session_state.selectbox_request_key = 0
ser_request_ids = df_data.index
selected_ref = st.sidebar.selectbox('Credit Application', ser_request_ids, index=0) #st.session_state.selectbox_request_key)

# Table with 2 columns
frame_left, frame_right = st.columns([3, 7])

# Display Selected Record
selected_record = df_data.loc[[selected_ref]] 
frame_right.dataframe(selected_record) 	

# Get score
def get_curl_command(df_sample, url) :
    str_features_values = df_sample.to_json(orient='split')
    str_data = '\'{"dataframe_split": ' + str_features_values + '}\' '
    return 'curl -d' + str_data + '''-H 'Content-Type: application/json' -X POST ''' + url

def get_li_scores(df_data) :
    df_X = df_data.drop('class', axis='columns')

    with open(dir_in + 'li_features.txt') as file_object:
        str_li_original_features = file_object.read()
        li_original_features = eval(str_li_original_features)

    df_X.columns = li_original_features
    str_curl = get_curl_command(df_X, 'localhost:5677/invocations')
    str_dict_predictions = subprocess.run(str_curl, shell=True, stdout=subprocess.PIPE, text=True).stdout
    frame_left.write(str_dict_predictions)
    dict_predictions = eval(str_dict_predictions) # {"predictions": [0]}
    li_predictions = dict_predictions['predictions']
    return li_predictions

li_float_scores = get_li_scores(df_data.iloc[:4])
frame_left.write(str(li_float_scores))

# Display Score Gauge
float_score = li_float_scores[0]
frame_left.plotly_chart(my.plot_gauge(100*float_score), use_container_width=True)

# Display All Data
bool_show_targets = st.checkbox('Show all data')	# STREAM: input Checkbox
if bool_show_targets :
	st.subheader('df_data')                         # STREAM: print Title
	st.dataframe(df_data, hide_index=True)          # STREAM: print Pandas
	
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
