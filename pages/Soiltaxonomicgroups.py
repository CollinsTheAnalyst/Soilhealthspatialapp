import streamlit as st
from sidebar import render_sidebar
from streamlit_option_menu import option_menu
import geemap
import geemap.foliumap as geemap
import ee

ee.Authenticate()
ee.Initialize(project='ee-collinsmwiti98')

st. set_page_config(page_title="Soil Taxonomic Groups", page_icon="🌱", layout="wide")
render_sidebar("Soil Taxonomic Groups")


st.title("Soil Taxonomic Groups")
col1, col2 = st.columns([4,1], gap="large", vertical_alignment="top", border=False, width="stretch")
options = list(["Soil Taxonomic Groups"])
index = options.index("Soil Taxonomic Groups")

with col2:
    selected = st.selectbox("Select Soil Taxonomic Groups", options, index=index)   

with col2:
    selected = st.selectbox("Select Soil Nutrient", options, index=index)

with col1:


    # Create a geemap map
    m = geemap.Map(
        basemap="HYBRID",
        plugin_Draw=True,
        Draw_export=True,
        locate_control=True,
    )

    # Load SoilGrids SOC dataset (example)
    soc = ee.Image("OpenLandMap/SOL/SOL_GRTGROUP_USDA-SOILTAX_C/v01")


    # Add soil organic carbon layer
    vis_params = {
        "min": 0,
        "max": 30,
        "palette": ["#ffffcc", "#41b6c4", "#253494"]  # yellow → teal → blue
    }
    m.addLayer(soc, vis_params, "Soil pH")

    # Center map over Kenya
    m.set_center(37.0, -1.0, 4)

    # Display map
    m.to_streamlit(height=850)