# ===========================================================   Init   ==============
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import shap
import matplotlib.pyplot as plt
import pickle

sys.path.insert(0, os.path.abspath('./utils'))
import my_functions as my                # Custom module	

# ===========================================================   Data   ============== 
# Dirs
dir_in  = './data/in/'
dir_out = './data/out/'

# Files
path_data         = dir_in  + 'data.csv'
path_X            = dir_in  + 'X_test_2.csv'
path_features     = dir_in  + 'li_features.txt'
path_waterfall      = dir_out + 'shap_waterfall.png'
path_shap_values  = dir_out + 'shap_values.npy'
path_explainer    = dir_out + 'explainer_X.pkl'

# Variables
li_features = my.get_li_features(path_features)
#li_old_features = list(df_selected_record.columns)
str_title = 'Local Feature Importance'
version_no = 1.0

str_author = 'Jean Vallée'

# Shortened fields' names
li_new_features = ['male', 'score_A', 'score_B', 'edu_level_2', 'edu_level_3', 'cash_loan', 'employee']
li_new_target   = ['class']
li_new_variables= li_new_features + li_new_target


# Pandas
df_data   = my.load_data(path_data)	
df_X      = my.load_data(path_X)[li_features]
df_data_0 = df_data[df_data['TARGET']==0]
df_data_1 = df_data[df_data['TARGET']==1]

# ===========================================================   SideBar   ===========
menu = st.sidebar

# Application Selection
ser_request_ids = sorted(df_data.index)
selected_ref = menu.selectbox('Credit Application N°', ser_request_ids, index=0) #st.session_state.selectbox_request_key)
# Selected Record
df_selected_record = df_data.loc[[selected_ref]] 
df_record_to_display = df_selected_record.copy()
df_record_to_display.columns = li_new_variables


# Display Score Gauge
## Get 1 score
float_1_score = my.get_li_scores(df_selected_record)[0]
#frame_left.write(str(float_1_score))
menu.html('<hr><h3 align="center">Score Class "1"</h3>')
menu.plotly_chart(my.plot_gauge(100*float_1_score, class_1=True), use_container_width=True)

menu.html('<hr><h3 align="center">Application\'s Features</h3>')
menu.dataframe(df_record_to_display.T, use_container_width=True)

menu.html(f'<hr> <p align="right">Version {version_no} <br> by <a href="https://jeanrosselvallee.github.io/">{str_author}</a></p>')


# ===========================================================   Main Frame   ========

st.html(f'<h2 align="center" style="color:lightblue;">{str_title}</h2>')
frame_left, frame_right = st.columns([3, 7])   # Divide Main Frame in 2

# Feature Importance 
st.html('<h3 align="center">Waterfall Graph</h3>')
## Shap Values
np_shap_values = my.load_np(path_shap_values)


# SHAP Explainer
@st.cache_data
def load_explainer() :
    with open(path_explainer, 'rb') as f:
        explainer_X = pickle.load(f)
    return explainer_X

## Graph Waterfall
row_number = df_X.index.get_loc(selected_ref)  
fig, ax = plt.subplots(figsize=(10, 4))
explainer_X = load_explainer()
shap.plots.waterfall(explainer_X[row_number]) #, max_display=7)
st.pyplot(fig)


# Analysis
st.html('<hr><h3 align="center">Interpretation</h3>')
frame_left_2, frame_right_2 = st.columns([5, 5])   # Divide Main Frame in 2 again
frame_left_2.write(
'''
1. Read the graph from a point at the bottom to another at the top  
- E[f(X)] on the X-axis represents the global average score of the population 
- f(X) on the top represents the target or predicted score

.

2. Progressively add up the SHAP value of each feature
- an arrow represents the SHAP value or its importance on the prediction
    - a red arrow has a positive impact 
    - a blue arrow has a negative impact
    - the arrow's length represents the feature's importance level
'''
)

frame_right_2.write(
'''
3. Notice that the order of the importance of features isn't the same for every prediction

.

4. The sign of the result of f(X) designates the predicted class 
    - negative means class "0"
    - positive means class "1"
'''
)
frame_right_2.markdown('##### Cf. [Interpretation Guide](https://www.aidancooper.co.uk/content/images/size/w1600/2021/11/beeswarm-1.png)👈')
