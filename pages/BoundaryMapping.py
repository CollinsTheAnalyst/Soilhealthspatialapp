import streamlit as st
from streamlit_option_menu import option_menu
import geemap.foliumap as geemap
from streamlit_folium import st_folium
import ee
from sidebar import render_sidebar
from shapely.geometry import shape
from shapely.ops import transform
from pyproj import Transformer

# Authenticate and initialize Earth Engine
ee.Authenticate()
ee.Initialize(project="ee-collinsmwiti98")

# Set page configurations
st.set_page_config(page_title="Field Boundary Mapping", page_icon="🌱", layout="wide")

render_sidebar("Boundary Mapping")

st.title("Field Boundary Mapping")

col1, col2 = st.columns([6,1], gap="medium", vertical_alignment="top", border=False, width="stretch")
options = list(["Field Boundary Mapping"])
index = options.index("Field Boundary Mapping")

with col2:
    selected = st.selectbox("Select Option", options, index=index)
    st.info("👉 Use the draw tool on the map to outline your field boundary.")

with col1:
    # Create a geemap map with draw tools
    m = geemap.Map(
        basemap="HYBRID",
        plugin_Draw=True,
        Draw_export=True,
        locate_control=True,
    )

    # Center map over Kenya
    m.set_center(37.0, -1.0, 8)

    # Use st_folium to capture drawn features
    map_data = st_folium(m, height=800, width="stretch")

    # Process drawn geometry
    if map_data and map_data.get("all_drawings"):
        st.subheader("📏 Field Boundary Details")

        # Get last drawn feature
        last_feature = map_data["all_drawings"][-1]
        geom = shape(last_feature["geometry"])

        # Reproject to UTM Zone 37S (Kenya, units in meters)
        transformer = Transformer.from_crs("epsg:4326", "epsg:32737", always_xy=True)
        geom_proj = transform(transformer.transform, geom)

        # Compute area & perimeter in meters
        area_m2 = geom_proj.area
        perimeter_m = geom_proj.length

        # Convert area to hectares and acres
        area_ha = area_m2 / 10_000
        area_acres = area_m2 / 4046.86

        # Display results
        st.success(f"**Area:** {area_ha:.2f} ha ({area_acres:.2f} acres)")

        
        
