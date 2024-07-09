# ===========================================================   Init   ==============
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import shap
import matplotlib.pyplot as plt
#import plotly.graph_objects as go
import json
import pickle
sys.path.insert(0, os.path.abspath('./utils'))
import my_functions as my                # Custom module	

Notes = '''
Current dir is project root's
'''
str_logo = '👨‍🏫'
str_title = str_logo + 'Dashboard'	     # MetaData
my.debug(str_title + ' - Version 0.0.2') 
#st.title(str_title) # STREAM: print Title
str_author = 'Jean Vallée'


# ===========================================================   Data   ============== 
# Dirs
dir_in  = './data/in/'
dir_out = './data/out/'

# Files
path_data         = dir_in  + 'data.csv'
path_X            = dir_in  + 'X_test_2.csv'
path_features     = dir_in  + 'li_features.txt'
path_violins      = dir_out + 'shap_violins.png'
path_shap_values  = dir_out + 'shap_values.npy'
path_explainer    = dir_out + 'explainer_X.pkl'
#path_log  = 

# Variables
li_features = my.get_li_features(path_features)

# Pandas
df_data   = my.load_data(path_data, 10)	
df_X      = my.load_data(path_X)[li_features]

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

# Feature Importance
## Shap Values
np_shap_values = my.load_np(path_shap_values)

## Global - Violins
@st.cache_data
def get_violins_image() :
    fig, ax = plt.subplots()
    shap.summary_plot(np_shap_values, df_X, feature_names=li_new_features, show=False)
    plt.savefig(path_violins)
    plt.close()
get_violins_image()
frame_right.image(path_violins)


'''
fig, ax = plt.subplots() #figsize=(3, 2))
shap.summary_plot(np_shap_values, df_X, feature_names=li_new_features, show=False)
frame_right.pyplot(fig)
'''

## Local - Waterfall
@st.cache_data
def load_explainer() :
    with open(path_explainer, 'rb') as f:
        explainer_X = pickle.load(f)
    return explainer_X

row_number = df_X.index.get_loc(selected_ref)  
fig, ax = plt.subplots(figsize=(3, 2))
explainer_X = load_explainer()
shap.plots.waterfall(explainer_X[row_number]) #, max_display=7)
frame_right.pyplot(fig)


# Display All Data
bool_show_targets = st.checkbox('Show all data')	# STREAM: input Checkbox
if bool_show_targets :
    st.subheader('df_data')                         # STREAM: print Title
    st.dataframe(df_data, hide_index=True)          # STREAM: print Pandas

    st.subheader('df_X')                         # STREAM: print Title
    st.dataframe(df_X)#, hide_index=True)          # STREAM: print Pandas
	
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
'''

'''
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
