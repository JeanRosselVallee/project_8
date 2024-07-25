'''
Index.py
Main page of Streamlit app
'''

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.abspath('./utils'))
import my_functions as my		# Custom module	

# Initialisation 
st.set_page_config(
	page_title="Hello",
	page_icon="👋",
	layout="wide"	
)
str_title = "Credit Application Dashboard"

# Sidebar
st.sidebar.image("https://www.whenthebanksaysno.co.uk/wp-content/uploads/2023/05/D9585792-ED4C-4363-900E-1EDCE31B99B1.jpeg")
st.sidebar.markdown(
	'''
	# About
	- [Web App URL](https://project8-ocr.streamlit.app/)
	- [GitHub Repository](https://github.com/JeanRosselVallee/project_8)
	''')
st.sidebar.markdown('[Streamlit Cheat-Sheet](https://cheat-sheet.streamlit.app/)')


# ================================= Main Frame ================
st.html(my.get_html_title(str_title, 'h2'))

frame_L, frame_R = st.columns(2)

# ================================= Left Frame ================

frame_L.markdown(
'''
### Contents 

|N°|Page|Graph|
|--|--|--|
|1| Global Feature Importance|Violins|
|2| Local Feature Importance|Waterfall|
|3| Simulation by Feature Tuning|KDE|
|4| Distribution of features A & B|KDE|
|4| Correlation of features A & B|Scatter Plot|

### Instructions
On the Sidebar, 
- Click on a page name
- Select the reference of the customer's credit application

'''
)
# ================================= Right Frame ================

frame_R.image('https://img.freepik.com/vecteurs-premium/icone-score-indicateur-credit-indique-niveau-solvabilite_485380-2529.jpg')
