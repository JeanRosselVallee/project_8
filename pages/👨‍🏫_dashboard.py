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
from matplotlib.colors import LinearSegmentedColormap

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
df_data   = my.load_data(path_data)	
df_X      = my.load_data(path_X)[li_features]
df_data_0 = df_data[df_data['TARGET']==0]
df_data_1 = df_data[df_data['TARGET']==1]

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
    fig, ax = plt.subplots(figsize=(10, 4))
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

## 2-Feature Select-Boxes
li_request_ids = li_old_features
str_feature_A = frame_left.selectbox('Feature A', li_request_ids, index=0)
str_feature_B = frame_left.selectbox('Feature B', li_request_ids, index=1)


## 2-Feature Distribution per class
for feature in [str_feature_A, str_feature_B] :
    x_curr  = df_selected_record[feature].values[0]
    fig, ax = plt.subplots(figsize=(10, 4))
    df_data_1[feature].plot.kde(ax=ax, color='red' , label='Class "1"')
    df_data_0[feature].plot.kde(ax=ax, color='blue', label='Class "0"')
    ax.axvline(x=x_curr, color='green', linestyle='--', label=f'Currrent observation = {x_curr}')
    ax.legend(), ax.set_xlabel(feature)
    frame_right.pyplot(fig)


## Scatter Plot
@st.cache_data   # Makes points visible by spreading them out
def spread_out(df_in, str_A, str_B, radius) :
    df_out_A = df_in[str_A] + np.random.normal(0, radius, size=df_in.shape[0])
    df_out_B = df_in[str_B] + np.random.normal(0, radius, size=df_in.shape[0])
    return df_out_A, df_out_B

str_x, str_y = str_feature_A, str_feature_B
df_A , df_B  = spread_out(df_X, str_x, str_y, radius = 0.15)

@st.cache_data   # Creates a custom color map
def make_cmap(bottom, low, high, top) : 
    li_colored_levels = [(0, bottom), (0.49, low), (0.51, high), (1, top)]
    return LinearSegmentedColormap.from_list('CustomMap', li_colored_levels)

np_y_pred_proba = np.load(dir_out + 'y_pred_proba.npy')

fig, ax = plt.subplots(figsize=(10, 4)) 
scatter_A_B = plt.scatter(  df_A, df_B, c=np_y_pred_proba, s=0.1, alpha=1, 
                            cmap=make_cmap('lightblue', 'darkblue', 'darkred', 'pink'))
plt.xlabel(str_x), plt.ylabel(str_y)
colorbar_scale = plt.colorbar(scatter_A_B, label='Target')
frame_right.pyplot(fig)


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


def spread_out(df_in, radius_in) :
    return df_in + np.random.normal(0, radius_in, size=df_in.shape[0])


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
