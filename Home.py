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
st.markdown("An app developed by for Soil Health and crop health Spatial Data Analysis.")   
