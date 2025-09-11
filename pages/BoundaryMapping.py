import streamlit as st
from streamlit_option_menu import option_menu
import geemap
import geemap.foliumap as geemap
import ee
import pandas as pd

ee.Authenticate()
ee.Initialize(project="ee-collinsmwiti98")

# Set page configurations
st.set_page_config(page_title="Field Boundary Mapping", page_icon="🌱", layout="wide")

st.sidebar.image("logo2.png", use_container_width=True)
st.sidebar.title("About")
st.sidebar.info("""An app developed by for Soil Health and crop health Spatial Data Analysis.""")

st.sidebar.title("Contact")
st.sidebar.info("""
Collins Mwiti|
0714326105 |
Collinskimathimwiti@gmail.com|
[GitHub](https://github.com/CollinsTheAnalyst) |   
[LinkedIn](https://www.linkedin.com/in/giswqs)
""")

st.header("Field Boundary Mapping")

col1,col2 = st.columns([4,1], gap="large", vertical_alignment="top", border=False, width="stretch")
options = list(["Field Boundary Mapping"])
index = options.index("Field Boundary Mapping")

with col2:
    selected = st.selectbox("Select Option", options, index=index)

with col1:
    # Create a geemap map
    m = geemap.Map(
        basemap="TERRAIN",
        plugin_Draw=True,
        Draw_export=True,
        locate_control=True,
    )

    # Center map over Kenya
    m.set_center(37.0, -1.0, 8)

    # Display the map in Streamlit
    m.to_streamlit(height=800)