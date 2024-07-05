# Init
import streamlit as st
import pandas as pd

# Debug Text
def print_debug(str_debug) :
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

