# Init
str_version = 'Version 0.0.1'
import streamlit as st
import pandas as pd
import numpy as np

# Left SideBar
st.sidebar.title("About")
st.sidebar.info("This multipage app template demonstrates various interactive web apps create")
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)
st.sidebar.html('\
    <hr> \
    <p align="right">' + str_version + '</p>')



markdown = """
1. Select a client's application for credit
2. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.
"""
st.markdown(markdown)


# Load data from URL
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data						# STREAM: Cache Function's Results
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Load data from file
path_csv = './data/in/y_test_2.csv'
try    : 
    df_y = pd.read(path_csv, 10)
    st.subheader('df_y')            # STREAM: print Subtitle
    st.write(df_y)                  # STREAM: print Pandas
except : 
    print('Could not open file', path_csv)

# Text
st_print1 = st.text('Loading data...')		# STREAM: print Text
data = load_data(10000)                 	# Load 10,000 rows
st_print1.text('Loading data...done!')		

# Markdown
st.markdown(								# STREAM: MarkDown
    """
    **👈 Simple Streamlit app** to see some examples
    of what Streamlit can do!
    ### See more complex demos
    - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
"""
)

# Condition
if st.checkbox('Show raw data'):			# STREAM: input Checkbox
	
# Table
	st.subheader('Raw data')				# STREAM: print Title
	st.write(data)						# STREAM: print Pandas

# Histogram
st.subheader('Number of pickups by hour')	
hist_values = np.histogram(					# Create Histogram
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0] 
st.bar_chart(hist_values)					# STREAM: plot Graph

# Slicer
hour_to_filter = st.slider('hour', 0, 23, 17)  # (min, max, default)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# Map
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)						# STREAM: plot Map




# Main
'''
st.title('simple_app')
number = st.slider("Pick a number", 0, 100)
st.write(f"You selected: {number}")
'''
