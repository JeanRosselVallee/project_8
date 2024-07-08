# Init
import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Debug Text
def debug(str_debug) :
    st.markdown(f':red[DEBUG: {str_debug}]')

# Load Data from File
@st.cache_data								# STREAM: Cache Function's Results
def load_data(file, nb_rows):
    try    : 
        df_contents = pd.read_csv(file, nrows=nb_rows).rename(columns={'Unnamed: 0': 'ref'}) 
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
	n_red      = n_curr / n_max
	n_green    = 1 - n_red
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
		height=100,
		margin=go.layout.Margin(l=2, r=2, b=2, t=2, pad=1)
	)
	return go.Figure(gauge, layout=layout)