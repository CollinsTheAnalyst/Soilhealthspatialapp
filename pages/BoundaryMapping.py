import streamlit as st
from streamlit_option_menu import option_menu
import geemap
import geemap.foliumap as geemap
import ee
import pandas as pd
from sidebar import render_sidebar

ee.Authenticate()
ee.Initialize(project="ee-collinsmwiti98")

# Set page configurations
st.set_page_config(page_title="Field Boundary Mapping", page_icon="🌱", layout="wide")

render_sidebar("Boundary Mapping")

st.title("Field Boundary Mapping")

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