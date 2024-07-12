'''
Index.py
Main page of Streamlit app
'''

import streamlit as st

st.set_page_config(
	page_title="Hello",
	page_icon="👋",
	layout="wide"	
)

# Customize the sidebar
st.sidebar.title("About")
st.sidebar.info("""
	Web App URL: <https://project8-ocr.streamlit.app/>
	GitHub Repository: <https://github.com/JeanRosselVallee/project_8>
	""")
st.sidebar.image("https://www.whenthebanksaysno.co.uk/wp-content/uploads/2023/05/D9585792-ED4C-4363-900E-1EDCE31B99B1.jpeg", width=50)

# Customize page title
st.title("Credit Application Dashboard")


st.image('https://img.freepik.com/vecteurs-premium/icone-score-indicateur-credit-indique-niveau-solvabilite_485380-2529.jpg')


st.markdown(
	'''
	- Credit Application Dashboard
	- Customer Profile
	- Simulation 
'''
)

st.markdown(
    """
    This multipage app template demonstrates various interactive web apps created using [streamlit](https://streamlit.io) and [leafmap](https://leafmap.org). It is an open-source project and you are very welcome to contribute to the [GitHub repository](https://github.com/giswqs/streamlit-multipage-template).
    """
)

st.header("Instructions")

markdown = """
1. Select a client's application for credit
2. Find your favorite emoji from https://emojipedia.org.
4. Add a new app to the `pages/` directory with an emoji in the file name, e.g., `1_🚀_Chart.py`.
"""
st.markdown(markdown)

st.sidebar.success("Success message")


