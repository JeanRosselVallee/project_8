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
st.write(str_version)


# Load data from URL
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data								# STREAM: Cache Function's Results
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Load data from file
path_csv = './data/in/y_test_2'
df_y = pd.read(path_csv)
st.subheader('df_y')				# STREAM: print Title
st.write(df_y)					# STREAM: print Pandas


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
