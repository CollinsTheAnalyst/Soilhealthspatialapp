import streamlit as st
from streamlit_option_menu import option_menu
import geemap
import geemap.foliumap as geemap
import ee

ee.Authenticate()
ee.Initialize(project='ee-collinsmwiti98')


# Set page configuration
st.set_page_config(page_title="GeoAgri Dashboard", page_icon="🌱", layout="wide")

st.sidebar.image("logo2.png", use_container_width=True)


st.sidebar.title("About")
st.sidebar.info("""
An app developed by for Soil Health and crop health Spatial Data Analysis.""")

st.sidebar.title("Contact")
st.sidebar.info("""
Collins Mwiti | 
0714326105 |
Collinskimathimwiti@gmail.com|
[GitHub](https://github.com/CollinsTheAnalyst) |   
[LinkedIn](https://www.linkedin.com/in/giswqs)
""")
    
st.title("Soil Map")

col1, col2 = st.columns([4,1], gap="large", vertical_alignment="top", border=False, width="stretch")
options = list(["N", "P", "K", "Ca", "Mg", "pH"])
index = options.index("pH")

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
    soc = ee.Image("ISDASOIL/Africa/v1/ph").select("mean_0_20")


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
    m.to_streamlit(height=800)

