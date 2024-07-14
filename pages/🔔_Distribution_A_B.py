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
str_title = 'Distribution of Features'
version_no = 1.0
str_author = 'Jean Vallée'

for k, v in st.session_state.items():
    st.session_state[k] = v

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

ser_request_ids = sorted(df_data.index)
selected_ref = menu.selectbox('Credit Application N°', ser_request_ids, key='shared_selectbox')

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

st.html(my.get_html_title(str_title, 'h2'))

frame_left, frame_right = st.columns([5, 5])


## 2-Feature Select-Boxes
li_old_features = list(df_X.head(1).columns)
li_request_ids = li_old_features
str_feature_A = frame_left.selectbox('Feature A', li_request_ids, index=0)
str_feature_B = frame_right.selectbox('Feature B', li_request_ids, index=1)


# 2-Feature Distribution per class
## Graphs
for idx, feature in enumerate([str_feature_A, str_feature_B]) :
    x_curr  = round(df_selected_record[feature].values[0], 2)
    fig, ax = plt.subplots(figsize=(5, 4))
    df_data_1[feature].plot.kde(ax=ax, color='red' , label='Class "1"')
    df_data_0[feature].plot.kde(ax=ax, color='blue', label='Class "0"')
    ax.axvline(x=x_curr, color='green', linestyle='--', label=f'Currrent value = {x_curr}')
    figure_legend = ax.legend()
    ax.set_xlabel(feature)
    if idx == 0 :   frame_left .pyplot(fig)
    else :          frame_right.pyplot(fig)


st.html('<hr>')

# Instructions
st.write(
'''
### Instructions
1. Select 2 Features to visualize their distribution
2. For each graph,
    - the blue curve is the distribution of Class "0"
    - the red curve  is the distribution of Class "1"
	- the green vertical line shows the feature value of the customer's credit application
3. In the scrolling list of the sidebar, search for the customer's application
4. Notice the 2-bell shape for binary categories centered on x=0 and x=1
'''
)
st.markdown('##### Cf. [Interpretation Guide](https://www.aidancooper.co.uk/content/images/size/w1600/2021/11/beeswarm-1.png)👈')
