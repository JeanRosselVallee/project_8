# ===========================================================   Init   ==============
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import shap
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath('./utils'))
import my_functions as my				# Custom module	

# ===========================================================   Data   ============== 
# Dirs
dir_in  = './data/in/'
dir_out = './data/out/'

# Files
path_data		 = dir_in  + 'data.csv'
path_X			= dir_in  + 'X_test_2.csv'
path_features	 = dir_in  + 'li_features.txt'
path_violins	  = dir_out + 'shap_violins.png'
path_shap_values  = dir_out + 'shap_values.npy'

# Variables
str_title = 'Simulation'
version_no = 1.0
str_author = 'Jean Vallée'


# Features
## Shortened fields' names
li_features = my.get_li_features(path_features)
li_variables = li_features + ['TARGET']
#li_new_features = ['male', 'score_A', 'score_B', 'edu_level_2', 'edu_level_3', 'cash_loan', 'employee']
#li_new_target   = ['class']
#li_new_variables= li_new_features + li_new_target


# Pandas
df_data   = my.load_data(path_data)	
df_X	  = my.load_data(path_X)[li_features]
df_data_0 = df_data[df_data['TARGET']==0]
df_data_1 = df_data[df_data['TARGET']==1]

# ===========================================================   SideBar   ===========
menu = st.sidebar

# Select Request Id
ser_request_ids = sorted(df_data.index)
selected_ref	= menu.selectbox('Credit Application N°', ser_request_ids, index=0) #st.session_state.selectbox_request_key)

# Select Record
df_selected_1  = df_data.loc[[selected_ref]] 
df_simulated_1 = df_selected_1.copy()
df_simulated_1.columns = li_variables

# Footer
menu.html(f'<hr> <p align="right">Version {version_no} <br> by <a href="https://jeanrosselvallee.github.io/">{str_author}</a></p>')


# ===========================================================   Main Frame   ========

#st.html(f'<h2 align="center" style="color:lightblue;">{str_title}</h2>')
st.html(my.get_html_title(str_title, 'h2'))


# DataFrames

## Actual
### 3-columns
#frame_top_L, frame_top_C, frame_top_R = st.columns(3)

st.html(my.get_html_title('Actual Record', 'b'))
st.dataframe(df_selected_1, hide_index=True)

## Simulated
#container_df_simulated = st.empty()   # Container = List of Items
container_df_simulated = st.container()

with container_df_simulated.container() : 
	st.html(my.get_html_title('Simulated Record', 'b'))   # Item #1
	if 'df_simulated_1' in st.session_state :
		df_simulated_1 = st.session_state['df_simulated_1'].copy()
	st.dataframe(df_simulated_1, hide_index=True)    # Item #2


# 2-columns
frame_L, frame_R = st.columns(2)


# ===========================================================   Left Frame   ========


## 2-Feature Select-Boxes
str_feature_A = frame_L.selectbox('Feature A', li_features, index=0)
str_feature_B = frame_R.selectbox('Feature B', li_features, index=1)
li_selected_features = [str_feature_A, str_feature_B]
li_selected_features_idx = [li_features.index(str_feature_A), li_features.index(str_feature_B)]

'''
# 2-Feature Distribution per class
## Graphs
for idx, feature in enumerate(li_selected_features) :
	x_curr  = df_selected_1[feature].values[0]
	fig, ax = plt.subplots(figsize=(5, 4))
	df_data_1[feature].plot.kde(ax=ax, color='red' , label='Class "1"')
	df_data_0[feature].plot.kde(ax=ax, color='blue', label='Class "0"')
	ax.axvline(x=x_curr, color='green', linestyle='--', label=f'Currrent observation = {x_curr}')
	figure_legend = ax.legend()
	ax.set_xlabel(feature)
	if idx == 0 :   frame_L.pyplot(fig)
	else :		  frame_R.pyplot(fig)
'''

# Sliders' Containers
container_slider_A = frame_L.container()
container_slider_B = frame_R.container()

# Gauges' Containers 

## Actual
frame_LL, frame_LR = frame_L.columns(2)
## Class "1"
container_gauge_actual_1 = frame_LL.container()
container_gauge_actual_1.html(my.get_html_title('Class "1"', 'h5'))
## Class "0"
container_gauge_actual_0 = frame_LR.container()
container_gauge_actual_0.html(my.get_html_title('Class "0"', 'h5'))

## Simulated
frame_RL, frame_RR = frame_R.columns(2)
## Class "1"
container_gauge_simul_1 = frame_RL.container()
container_gauge_simul_1.html(my.get_html_title('Class "1"', 'h5'))
## Class "0"
container_gauge_simul_0 = frame_RR.container()
container_gauge_simul_0.html(my.get_html_title('Class "0"', 'h5'))

# Gauges

## Actual
float_1_score = my.get_li_scores(df_selected_1)[0]
## Class "1"
container_gauge_actual_1.plotly_chart(my.plot_gauge(100*float_1_score, class_1=True), use_container_width=True)
## Class "0"
container_gauge_actual_0.plotly_chart(my.plot_gauge(100*float_1_score, class_1=False), use_container_width=True)

## Simulated
## Class "1"
container_gauge_simul_1.plotly_chart(my.plot_gauge(100*float_1_score, class_1=True), use_container_width=True)
## Class "0"
container_gauge_simul_0.plotly_chart(my.plot_gauge(100*float_1_score, class_1=False), use_container_width=True)

# Sliders
li_features_float = my.get_1_type_cols_list(df_simulated_1, 'float64')

for selected_idx, selected_feature in enumerate(li_selected_features) :
	if selected_feature in li_features_float : min_value, max_value = 0.0, 1.0
	else : min_value, max_value = 0, 1
	
	initial_value = df_simulated_1[selected_feature].values[0]
	#st.session_state['selected_feature'] = selected_feature
	#st.session_state['df_simulated_1'] = df_simulated_1
	
	
	if selected_idx == 0 :  frame_slider = container_slider_A
	else :		  			frame_slider = container_slider_B
	#my.plot_slider(li_features, li_new_features, selected_idx, box, frame_left, initial_value, min_value, max_value)
	my.plot_slider(	df_simulated_1, selected_feature, initial_value,
					frame_slider, container_gauge_simul_1, container_gauge_simul_0, container_df_simulated)


# Instructions
st.html('<hr><h3 align="center">Instructions</h3>')
frame_L_2, frame_R_2 = st.columns(2)   # Divide Main Frame in 2 again
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
