# ===========================================================   Init   ==============
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import shap
import matplotlib.pyplot as plt

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
path_violins      = dir_out + 'shap_violins.png'
path_shap_values  = dir_out + 'shap_values.npy'

# Variables
li_features = my.get_li_features(path_features)
str_title = 'Simulation'
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
#frame_L.write(str(float_1_score))
menu.html('<hr><h3 align="center">Score Class "1"</h3>')
menu.plotly_chart(my.plot_gauge(100*float_1_score, class_1=True), use_container_width=True)

menu.html('<hr><h3 align="center">Application\'s Features</h3>')
menu.dataframe(df_record_to_display.T, use_container_width=True)

menu.html(f'<hr> <p align="right">Version {version_no} <br> by <a href="https://jeanrosselvallee.github.io/">{str_author}</a></p>')


# ===========================================================   Main Frame   ========

st.html(f'<h2 align="center" style="color:lightblue;">{str_title}</h2>')
frame_L, frame_R = st.columns([5, 5])

frame_L.dataframe(df_record_to_display)


frame_LL, frame_LR = frame_L.columns([5, 5])
# Display Score Gauge
frame_LL.html(f'<h4 align="center" style="color:lightblue;">Class "1"</h4>')
frame_LL.plotly_chart(my.plot_gauge(100*float_1_score, class_1=True), use_container_width=True)
frame_LR.html(f'<h4 align="center" style="color:lightblue;">Class "0"</h4>')
frame_LR.plotly_chart(my.plot_gauge(100*float_1_score, class_1=False), use_container_width=True)



## 2-Feature Select-Boxes
li_old_features = list(df_X.head(1).columns)
li_request_ids = li_old_features
str_feature_A = frame_L.selectbox('Feature A', li_request_ids, index=0)
str_feature_B = frame_R.selectbox('Feature B', li_request_ids, index=1)
li_selected_features = [str_feature_A, str_feature_B]
li_selected_features_idx = [li_old_features.index(str_feature_A), li_old_features.index(str_feature_B)]


# 2-Feature Distribution per class
## Graphs
for idx, feature in enumerate(li_selected_features) :
    x_curr  = df_selected_record[feature].values[0]
    fig, ax = plt.subplots(figsize=(5, 4))
    df_data_1[feature].plot.kde(ax=ax, color='red' , label='Class "1"')
    df_data_0[feature].plot.kde(ax=ax, color='blue', label='Class "0"')
    ax.axvline(x=x_curr, color='green', linestyle='--', label=f'Currrent observation = {x_curr}')
    figure_legend = ax.legend()
    ax.set_xlabel(feature)
    if idx == 0 :   frame_L.pyplot(fig)
    else :          frame_R.pyplot(fig)


df_simulated_record = df_selected_record.copy()
# Sliders
li_features_float = my.get_1_type_cols_list(df_record_to_display, 'float64')
for idx, feature_name in enumerate(li_selected_features) :
    feature_idx  = li_selected_features_idx[idx]
    new_feature_name = li_new_features[feature_idx]
    default_value = df_record_to_display[new_feature_name].values[0]
    if new_feature_name in li_features_float : min_value, max_value = 0.0, 1.0
    else : min_value, max_value = 0, 1
    #st.session_state['feature_name'] = feature_name
    #st.session_state['df_simulated_record'] = df_simulated_record
    
    
    if idx == 0 :   frame_slider = frame_L
    else :          frame_slider = frame_R
    #my.plot_slider(li_old_features, li_new_features, idx, frame_right, frame_left, default_value, min_value, max_value)
    my.plot_slider(df_simulated_record, li_old_features, li_new_features, idx, frame_slider, frame_R, default_value, min_value, max_value)


# Instructions
st.html('<hr><h3 align="center">Instructions</h3>')
frame_L_2, frame_R_2 = st.columns([5, 5])   # Divide Main Frame in 2 again
frame_L_2.write(
'''
1. Scores from external sources are the most influential of attributes

2. Characterisation of a bad borrower:
    - low scores from external sources
    - no higher education
    - male
    - apply for a cash loan
    - employee
    - secondary education
'''
)

frame_R_2.write(
'''
3. Suggestions to improve chances of a credit approval:
    - don't apply for a cash loan
    - get a higher education degree

4. Most frequent values :        
    - high scores from external sources
    - no higher education
    - female
    - applications for cash loans
    - employee
    - secondary education
'''
)
st.markdown('##### Cf. [Interpretation Guide](https://www.aidancooper.co.uk/content/images/size/w1600/2021/11/beeswarm-1.png)👈')
