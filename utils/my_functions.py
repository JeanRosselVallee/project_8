# Init
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import subprocess

# Debug Text
def debug(str_debug) :
    st.markdown(f':red[DEBUG: {str_debug}]')

# Load Data from File
#@st.cache_data								# STREAM: Cache Function's Results
def load_data(file, nb_rows):
    try    : 
        df_contents = pd.read_csv(file, nrows=nb_rows).rename(columns={'Unnamed: 0': 'request_id'}) 
        #.drop('Unnamed: 0', axis='columns')
        return df_contents
    except Exception as e: 
        st_text0 = st.text(f'Could not open file {file}: {e}')
        df_empty = pd.DataFrame([])
        return df_empty

def plot_gauge(n_curr) :
	li_markers = [20, 40, 60, 80]
	li_labels  = [str(n) for n in li_markers]
	n_max      = 100
	n_green    = n_curr / n_max
	n_red      = 1 - n_green
	color_curr = f'rgb( {n_red}, {n_green},0)'
	gauge = go.Indicator(
		mode    = "gauge+number",
		value   = n_curr,
		number  = {'suffix': "%"},
		domain  = {'x': [0, 1], 'y': [0, .8]},
		gauge={'axis'     : {'range': [None, n_max], 'tickvals': li_markers, 'ticktext': li_labels},
			   'bar'      : {'color': color_curr, 'thickness': 1},
			   'threshold': {'line': {'color': 'black', 'width': 2}, 'thickness': 1, 'value': n_curr}
			   },
	)
	layout     = go.Layout(
		height = 100,
		margin = go.layout.Margin(l=2, r=2, b=2, t=2, pad=1)
	)
	return go.Figure(gauge, layout=layout)

# Get score
def get_curl_command(df_sample, url) :
    str_features_values  = df_sample.to_json(orient='split')
    str_data             = '\'{"dataframe_split": ' + str_features_values + '}\' '
    return 'curl -d' + str_data + '''-H 'Content-Type: application/json' -X POST ''' + url

def get_li_scores(df_data_sample) :
    df_X_sample          = df_data_sample.drop('TARGET', axis='columns')
    str_curl             = get_curl_command(df_X_sample, 'localhost:5677/invocations')
    str_dict_predictions = subprocess.run(str_curl, shell=True, stdout=subprocess.PIPE, text=True).stdout
    dict_predictions     = eval(str_dict_predictions) # {"predictions": [0]}
    li_predictions       = dict_predictions['predictions']
    return li_predictions

def get_1_type_cols_list(df_in, type_in) :
    ''' Lists all columns in a Pandas of a given type '''
    ser_cols_types = df_in.dtypes
    return list(ser_cols_types[ser_cols_types==type_in].index)

# Slider's Callback Function : Display Simulated Score
def display_simulated_score(idx_feature, li_features, frame) :
    new_value = eval('st.session_state.slider_value_' + str(idx_feature))
    feature = li_features[idx_feature]
    df_1_record = st.session_state['df_simulated_record'].copy()
    df_1_record[feature] = new_value
    debug(feature + '=' + str(new_value))
    frame.dataframe(df_1_record, hide_index=True)  
    float_1_score = get_li_scores(df_1_record)[0]
    frame.plotly_chart(plot_gauge(100*float_1_score), use_container_width=True)
    st.session_state['df_simulated_record'] = df_1_record.copy()

# slider
def plot_slider(li_old_features, li_new_features, feature_idx, frame_slider, frame_gauge, val_default, val_min, val_max) :
    value_out = frame_slider.slider(li_new_features[feature_idx], val_min, val_max,   # (min, max, default)
                    val_default, on_change=display_simulated_score, args=[feature_idx, li_old_features, frame_gauge],
                    key='slider_value_' + str(feature_idx))
    #return value_out
