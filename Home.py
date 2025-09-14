import streamlit as st
from streamlit_option_menu import option_menu

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


    
st.title("🌱 GeoAgri Dashboard")

st.markdown(
    """
    The **GeoAgri Dashboard** is an interactive web application designed to support 
    **soil health, crop health, and spatial data analysis** for farmers, agronomists, and researchers.  
    It integrates [Streamlit](https://streamlit.io) with open-source geospatial libraries, including 
    [Leafmap](https://leafmap.org), [Geemap](https://geemap.org), and [Folium](https://python-visualization.github.io/folium/).  

    Key features include:  
    - 🌍 NDVI/EVI vegetation analysis  
    - 🌱 Soil nutrient dashboards (ISDA)
    - 🌦️ Weather data visualization
    - 🌾 Crop nutrient requirements  
    - 🐛 Plant Disease Detection 
    - 📊 Soil nutrient removal values  
    - 🗺️ Field Boundary mapping 
 
    """
)


st.subheader("Timelapse of Satellite Imagery")



row1_col1, row1_col2 = st.columns(2)
with row1_col1:
    st.image("Data\\spain.gif")

with row1_col2:
    st.image("Data\\goes.gif")



st.markdown(
    """
    <p style= font-size:18px;'>
    <i>The data aims to empower users with actionable insights for sustainable agriculture and improved crop yields.</i>
    </p>
    """,
    unsafe_allow_html=True
)
