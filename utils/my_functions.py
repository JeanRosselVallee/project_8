# Init
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import subprocess
import shap
import matplotlib.pyplot as plt
import platform

# Variables
host = 'http://34.155.188.3/'

# Debug Text
def debug(str_debug) :
	str_message = f':red[DEBUG: {str_debug}]'
	st.markdown(str_message)
	with open('./log/streamlit_app.log', 'a') as f:
		print(str_message, file=f)

# Load Data from File
@st.cache_data								# STREAM: Cache Function's Results
def load_data(file, nb_rows=-1):
	try	: 
		if nb_rows > 0 :    df_contents = pd.read_csv(file, nrows=nb_rows)
		else :				df_contents = pd.read_csv(file)
		df_contents = df_contents	.rename(columns={'Unnamed: 0': 'request_id'}) \
									.set_index('request_id')
		#.drop('Unnamed: 0', axis='columns')
		return df_contents
	except Exception as e: 
		st_text0 = st.text(f'Could not open file {file}: {e}')
		df_empty = pd.DataFrame([])
		return df_empty

def plot_gauge(n_curr, class_1=True) :
	li_markers = [20, 40, 60, 80]
	li_labels  = [str(n) for n in li_markers]
	n_max	  = 100
	n_red	= n_curr / n_max
	n_green	  = 1 - n_red
	color_curr = f'rgb( {n_red}, {n_green},0)'
	if not class_1 : n_curr = n_max - n_curr
	gauge = go.Indicator(
		mode	= "gauge+number",
		value   = n_curr,
		number  = {'suffix': "%"},
		domain  = {'x': [0, 1], 'y': [0, .8]},
		gauge={'axis'	  : {'range': [None, n_max], 'tickvals': li_markers, 'ticktext': li_labels},
			   'bar'	  : {'color': color_curr, 'thickness': 1},
			   'threshold': {'line': {'color': 'black', 'width': 2}, 'thickness': 1, 'value': n_curr}
			   },
	)
	layout	 = go.Layout(
		height = 75,
		margin = go.layout.Margin(l=2, r=2, b=2, t=2, pad=1)
	)
	return go.Figure(gauge, layout=layout)

# Get score
def get_curl_command(df_sample, url) :
	str_features_values  = df_sample.to_json(orient='split')
	str_data			 = '\'{"dataframe_split": ' + str_features_values + '}\' '
	return 'curl -d' + str_data + '''-H 'Content-Type: application/json' -X POST ''' + url


def get_1_type_cols_list(df_in, type_in) :
	''' Lists all columns in a Pandas of a given type '''
	ser_cols_types = df_in.dtypes
	return list(ser_cols_types[ser_cols_types==type_in].index)
	
def get_li_scores(df_data_sample) :
	df_X_sample		  = df_data_sample.drop('TARGET', axis='columns')
	str_curl			 = get_curl_command(df_X_sample, host + ':5677/invocations')
	
	str_operating_system = str(platform.system())
	if str_operating_system == 'Windows' :  # In Windows, add \ before quotes
		str_curl = str_curl.replace('"', '\\"').replace('\'', '"')
	
	str_dict_predictions = subprocess.run(str_curl, shell=True, stdout=subprocess.PIPE, text=True).stdout 
	#st.warning('str_dict_predictions=[' + str_dict_predictions + ']')
	dict_predictions	 = eval(str_dict_predictions) # {"predictions": [0]}
	li_predictions	   = dict_predictions['predictions']
	return li_predictions

# Slider's Callback Function : Display Simulated Score
def display_simulated_score(df_sample_1, feature, container_gauge_1, container_gauge_0, container_df) :
	new_value = eval('st.session_state.slider_value_' + feature)

	if 'df_simulated_record' in st.session_state :
		df_1_record = st.session_state['df_simulated_record'].copy()
	else :
		df_1_record = df_sample_1
	
	
	df_1_record[feature] = new_value
	# st.write(feature + '=' + str(new_value))
	
	with container_df.container() :
		st.dataframe(df_1_record, hide_index=True)  
	
	
	
	float_1_score = get_li_scores(df_1_record)[0]
	container_gauge_1.plotly_chart(plot_gauge(100*float_1_score, class_1=True), use_container_width=True)
	container_gauge_0.plotly_chart(plot_gauge(100*float_1_score, class_1=False), use_container_width=True)
	st.session_state['df_simulated_record'] = df_1_record.copy()

# Plot sliders
def plot_slider(	df_sample_1, feature, curr_value,
					frame_slider, container_gauge_1, container_gauge_0, container_df) :

	li_features_float = get_1_type_cols_list(df_sample_1, 'float64')
	if feature in li_features_float :   min_value, max_value = 0.0, 1.0
	else : 								min_value, max_value =   0,   1
	
	
	frame_slider.slider(	'Tune feature\'s value :', min_value, max_value, curr_value,   # (min, max, default)
							on_change=display_simulated_score, 
								args=[	df_sample_1, feature, 
										container_gauge_1, container_gauge_0, container_df],
							key='slider_value_' + feature)

# Get df_X features
def get_li_features(path) :
	with open(path) as f:
		str_li_features = f.read()
	li_features = eval(str_li_features)
	return li_features

@st.cache_data
def load_np(path) : return np.load(path) # One-shot load from file

def get_html_title(str_text, str_tag) :
	return f'<{str_tag} align="center" style="color:lightblue;">{str_text}</{str_tag}>'
