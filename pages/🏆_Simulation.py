# ===========================================================   Init   ==============
import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import shap
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.abspath('./utils'))
import my_functions as my		# Custom module	

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
str_title = 'Feature Tuning'
version_no = 1.0
str_author = 'Jean Vallée'

for k, v in st.session_state.items():
    st.session_state[k] = v


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

ser_request_ids = sorted(df_data.index)
selected_ref = menu.selectbox('Credit Application N°', ser_request_ids, key='shared_selectbox')

# Select Record
df_selected_1  = df_data.loc[[selected_ref]] 
df_simulated_1 = df_selected_1.copy()
df_simulated_1.columns = li_variables

# Display Graphs
bool_show_graphs = menu.checkbox('Show features\' values on distribution graphs')

# Footer
menu.html(f'<hr> <p align="right">Version {version_no} <br> by <a href="https://jeanrosselvallee.github.io/">{str_author}</a></p>')


# ===========================================================   Main Frame   ========

# Headers

### 3-columns
frame_top_1, frame_top_2, frame_top_3 = st.columns([27, 8, 8])
frame_top_1.html(my.get_html_title(str_title, 'h5'))
frame_top_2.html(my.get_html_title('Class "1"', 'h5'))
frame_top_3.html(my.get_html_title('Class "0"', 'h5'))

# Records

## Actual
float_1_score = my.get_li_scores(df_selected_1)[0]
### 4-columns
zone_actual_1, zone_actual_2, zone_actual_3, zone_actual_4 = st.columns([3, 24, 8, 8])
zone_actual_1.html(my.get_html_title('Actual', 'b'))
zone_actual_2.dataframe(df_selected_1, hide_index=True)
zone_actual_3.plotly_chart(my.plot_gauge(100*float_1_score, class_1=True), use_container_width=True)
zone_actual_4.plotly_chart(my.plot_gauge(100*float_1_score, class_1=False))

st.html(f'<hr>')

## Simulated
### 4-columns
zone_simul_1, zone_simul_2, zone_simul_3, zone_simul_4 = st.columns([3, 24, 8, 8])
zone_simul_1.html(my.get_html_title('Simulation', 'b'))
container_df_simulated = zone_simul_2.container()

## Simulated

# 2-columns
frame_L, frame_R = st.columns(2)

## Selection Boxes
str_feature_A = frame_L.selectbox('Feature A', li_features, index=0)
str_feature_B = frame_R.selectbox('Feature B', li_features, index=1)
li_selected_features = [str_feature_A, str_feature_B]
li_selected_features_idx = [li_features.index(str_feature_A), li_features.index(str_feature_B)]


# Sliders

# Sliders' Containers
container_slider_A = frame_L.container()
container_slider_B = frame_R.container()

li_features_float = my.get_1_type_cols_list(df_simulated_1, 'float64')

for selected_idx, selected_feature in enumerate(li_selected_features) :
	if selected_feature in li_features_float : min_value, max_value = 0.0, 1.0
	else : min_value, max_value = 0, 1
	
	initial_value = df_simulated_1[selected_feature].values[0]	
	
	if selected_idx == 0 :  frame_slider = container_slider_A
	else :		  			frame_slider = container_slider_B
	my.plot_slider(	df_simulated_1, selected_feature, initial_value,
					frame_slider, zone_simul_3, zone_simul_4, container_df_simulated)


# Feature Distribution per class
## Graphs
if bool_show_graphs :
	for idx, feature in enumerate(li_selected_features) :
		x_actual = round(df_selected_1[feature].values[0], 2)
		if ('slider_value_' + feature) in st.session_state :
				x_simul  = round(eval('st.session_state.slider_value_' + feature), 2)
		else :  x_simul  = x_actual
		fig, ax  = plt.subplots(figsize=(10, 3))
		ax.axvline(x=x_simul,  color='orange', linestyle='--', label=f'Simulated value= {x_simul}')
		ax.axvline(x=x_actual, color='gray',  linestyle='--', label=f'Actual        value= {x_actual}')
		df_data_0[feature].plot.kde(ax=ax, color='blue', label='Class "0"')
		df_data_1[feature].plot.kde(ax=ax, color='red' , label='Class "1"')
		figure_legend = ax.legend()
		ax.set_xlabel(feature)
		if idx == 0 :   frame_L.pyplot(fig)
		else :		    frame_R.pyplot(fig)


st.html('<hr>')

# Instructions
frame_left_2, frame_right_2 = st.columns([5, 5])   # Divide Main Frame in 2 again
frame_left_2.write(
'''
### Scenario
The banker shows a customer how to increase the chances for an approval of his credit application

### Goal
The banker finds a combination of features' values that
- decreases the score of Class "0" (bad  borrowers), or,	
- increases the score of Class "1" (good borrowers)
'''
)

frame_right_2.write(
'''
### Instructions
1. In the scrolling list of the sidebar, search for the customer's application
2. Select features to tune in 2 by 2
3. Use the slider to update the features' values
4. Suggestions to improve chances of a credit approval:
    - don't apply for a cash loan
    - get a higher education degree

.
	
##### Cf. [Interpretation Guide](https://www.aidancooper.co.uk/content/images/size/w1600/2021/11/beeswarm-1.png)👈
'''
)
