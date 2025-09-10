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
    
st.title("🌱 NDVI/EVI Analysis")

col1, col2 = st.columns([4,1], gap="large", vertical_alignment="top", border=False, width="stretch")
options = list(["NDVI", "EVI"])
index = options.index("NDVI")

with col2:
    selected = st.selectbox("Select Vegetation Index", options, index=index)

with col1:

    # Create a map with Google Hybrid as default basemap
    m = geemap.Map(
        basemap="HYBRID", 
        plugin_Draw=True,
        Draw_export=True,
        locate_control=True,
    )

    # Center map (example: Nairobi)
    m.set_center(37.0, -1.0, 8)

    # Display the map in Streamlit
    m.to_streamlit(height=800)
