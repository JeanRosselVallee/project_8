'''
Index.py
Main page of Streamlit app
'''

import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Welcome to Streamlit! 👋")

st.sidebar.success("Select a demo above.")

st.markdown(
	'''
	# Credit Application Dashboard
	- Customer Profile
	- Simulation 
'''
)


