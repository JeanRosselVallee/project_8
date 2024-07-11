# ===========================================================   Init   ==============
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import plotly.graph_objects as go
import json

sys.path.insert(0, os.path.abspath('./utils'))
import my_functions as my				# Custom module	

Notes = '''
Current dir is project root's
'''
str_logo = '👨‍🏫'
str_title = str_logo + 'Dashboard'	   # MetaData
#my.debug(str_title + ' - Version 0.0.2') 
#st.title(str_title) # STREAM: print Title
str_author = 'Jean Vallée'


# ===========================================================   Data   ============== 
## Load
dir_in = './data/in/'
path_data = dir_in + 'data.csv'
df_data   = my.load_data(path_data, 10) 
#df_data.set_index('request_id', inplace=True)


# ===========================================================   SideBar   ===========
menu = st.sidebar
menu.title(str_title)
menu.info('Customer profile with main features')

# Application Selection
#if 'selectbox_request_key' not in st.session_state : st.session_state.selectbox_request_key = 0
ser_request_ids = df_data.index
selected_ref = st.sidebar.selectbox('Credit Application', ser_request_ids, index=0) #st.session_state.selectbox_request_key)


# ===========================================================   Main  ===============
# Table with 2 columns
frame_left, frame_right = st.columns([3, 7])


# ===========================================================   Left Frame   ========
# Display Selected Record
df_selected_record = df_data.loc[[selected_ref]] 
df_record_to_display = df_selected_record.copy()

# Shortened fiedls' names
li_old_features = list(df_selected_record.columns)
li_new_features = ['male', 'score_A', 'score_B', 'edu_level_2', 'edu_level_3', 'cash_loan', 'employee']
li_new_target   = ['class']
li_new_variables= li_new_features + li_new_target
df_record_to_display.columns = li_new_variables



# ===========================================================   Right Frame   =======

frame_right.dataframe(df_record_to_display)	 

# Get 1 score
float_1_score = my.get_li_scores(df_selected_record)[0]
#frame_left.write(str(float_1_score))

# Get scores' list
#li_float_scores = my.get_li_scores(df_data.iloc[:4])
#frame_left.write(str(li_float_scores))

# Display Score Gauge
frame_left.plotly_chart(my.plot_gauge(100*float_1_score), use_container_width=True)

# Display All Data
bool_show_targets = st.checkbox('Show all data')	# STREAM: input Checkbox
if bool_show_targets :
	st.subheader('df_data')						 # STREAM: print Title
	st.dataframe(df_data, hide_index=True)		  # STREAM: print Pandas
	
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


df_simulated_record = df_selected_record.copy()

li_features_float = my.get_1_type_cols_list(df_record_to_display, 'float64')
for idx, feature_name in enumerate(li_new_features) :
	default_value = df_record_to_display[feature_name].values[0]
	if feature_name in li_features_float : min_value, max_value = 0.0, 1.0
	else : min_value, max_value = 0, 1
	#st.session_state['feature_name'] = feature_name
	#st.session_state['df_simulated_record'] = df_simulated_record
	
	
	#my.plot_slider(li_old_features, li_new_features, idx, frame_right, frame_left, default_value, min_value, max_value)
	my.plot_slider(df_simulated_record, li_old_features, li_new_features, idx, frame_right, frame_left, default_value, min_value, max_value)
