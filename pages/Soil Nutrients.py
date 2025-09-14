import streamlit as st
from sidebar import render_sidebar
from streamlit_option_menu import option_menu
import geemap
import geemap.foliumap as geemap
import ee

ee.Authenticate()
ee.Initialize(project='ee-collinsmwiti98')

ph = ee.Image("ISDASOIL/Africa/v1/ph").select('mean_0_20').divide(10);
nitrogen = ee.Image("ISDASOIL/Africa/v1/nitrogen_total").select('mean_0_20').divide(100).exp().subtract(1);
phosphorous = ee.Image("ISDASOIL/Africa/v1/phosphorus_extractable").select('mean_0_20').divide(10).exp().subtract(1);
potassium = ee.Image("ISDASOIL/Africa/v1/potassium_extractable").select('mean_0_20').divide(10).exp().subtract(1);
calcium = ee.Image("ISDASOIL/Africa/v1/calcium_extractable").select('mean_0_20').divide(10).exp().subtract(1);
magnesium = ee.Image("ISDASOIL/Africa/v1/magnesium_extractable").select('mean_0_20').divide(10).exp().subtract(1);
cec = ee.Image("ISDASOIL/Africa/v1/cation_exchange_capacity").select('mean_0_20').divide(10).exp().subtract(1);
iron = ee.Image("ISDASOIL/Africa/v1/iron_extractable").select('mean_0_20').divide(10).exp().subtract(1);
carbon = ee.Image("ISDASOIL/Africa/v1/organic_carbon").select('mean_0_20').divide(10).exp().subtract(1);

# Set page configuration
st.set_page_config(page_title="GeoAgri Dashboard", page_icon="🌱", layout="wide")

render_sidebar("Soil Nutrient")
    
st.title("Soil Map")

col1, col2 = st.columns([4,1], gap="large", vertical_alignment="top", border=False, width="stretch")
nutrient_dict = {
    "pH": ph,
    "N": nitrogen,
    "P": phosphorous,
    "K": potassium,
    "Ca": calcium,
    "Mg": magnesium,
    "CEC": cec,
    "Fe": iron,
    "Carbon": carbon,
}

vis_params = {
    "pH": {"min": 4, "max": 9, "palette": ["red", "yellow", "green"]},
    "N": {"min": 0, "max": 1, "palette": ["#ffffcc", "#41b6c4", "#253494"]},
    "P": {"min": 0, "max": 30, "palette": ["#f7fcf5", "#41ab5d", "#00441b"]},
    "K": {"min": 0, "max": 30, "palette": ["#fff7ec", "#fc8d59", "#7f0000"]},
    "Ca": {"min": 0, "max": 30, "palette": ["#f1eef6", "#74a9cf", "#045a8d"]},
    "Mg": {"min": 0, "max": 20, "palette": ["#ffffb2", "#fd8d3c", "#bd0026"]},
    "CEC": {"min": 0, "max": 40, "palette": ["#f7fcb9", "#addd8e", "#31a354"]},
    "Fe": {"min": 0, "max": 20, "palette": ["#fee5d9", "#fcae91", "#a50f15"]},
    "Carbon": {"min": 0, "max": 5, "palette": ["#ffffcc", "#41b6c4", "#253494"]},
}

options = list(nutrient_dict.keys())


with col2:
    selected = st.selectbox("Select Soil Nutrient", options, index=0)

with col1:
    m = geemap.Map(
        basemap="HYBRID",
        plugin_Draw=True,
        Draw_export=True,
        locate_control=True,
    )
    # Load the selected nutrient layer
    nutrient_layer = nutrient_dict[selected]

    # Get the visualization params for that nutrient
    vis = vis_params[selected]

    # Add nutrient layer to map
    m.addLayer(nutrient_layer, vis, f"Soil {selected}")

    # Center map over Kenya
    m.set_center(37.0, -1.0, 4)

    # Display map
    m.to_streamlit(height=600)

