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
str_title = 'Correlation of Features'
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
frame_left, frame_right = st.columns([5, 5])


## 2-Feature Select-Boxes
li_old_features = list(df_X.head(1).columns)
li_request_ids = li_old_features
str_feature_A = frame_left.selectbox('Feature A', li_request_ids, index=0)
str_feature_B = frame_right.selectbox('Feature B', li_request_ids, index=1)


# 2-Feature Distribution per class
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
label_x, label_y = plt.xlabel(str_x), plt.ylabel(str_y)
colorbar_scale = plt.colorbar(scatter_A_B, label='Target')
st.pyplot(fig)



# Instructions
st.html('<hr><h3 align="center">Instructions</h3>')
frame_left_2, frame_right_2 = st.columns([5, 5])   # Divide Main Frame in 2 again
frame_left_2.write(
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

frame_right_2.write(
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
