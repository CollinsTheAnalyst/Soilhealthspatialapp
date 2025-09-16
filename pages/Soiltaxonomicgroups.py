import streamlit as st
from sidebar import render_sidebar
from streamlit_option_menu import option_menu
import geemap
import geemap.foliumap as geemap
import ee
import folium
from geopy.geocoders import Nominatim

# Initialize geopy geocoder
geolocator = Nominatim(user_agent="soil_nutrient_app")
def get_location_name(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), language="en")
        if location and "display_name" in location.raw:
            return location.raw["display_name"].split(",")[0]  # first part (village/town)
        elif location:
            return location.address.split(",")[0]
        else:
            return "Unknown location"
    except Exception:
        return "Location lookup failed"
    
ee.Authenticate()
ee.Initialize(project='ee-collinsmwiti98')

st. set_page_config(page_title="Soil Taxonomic Groups", page_icon="🌱", layout="wide")
render_sidebar("Soil Taxonomic Groups")

kenya_counties = ee.FeatureCollection("projects/ee-collinsmwiti98/assets/KenyaCounties")
county_names = kenya_counties.aggregate_array("COUNTY").distinct().getInfo()


st.title("Soil Taxonomic Groups")
col1, col2 = st.columns([4,1], gap="medium")

with col2:
    selected_county = st.selectbox("Select County", county_names)
    county_fc = kenya_counties.filter(ee.Filter.eq("COUNTY", selected_county))

    st.info("Please select a point on the map to view detailed soil data for the location.")

with col1:
    # Get county center dynamically
    county_bounds = county_fc.geometry().bounds()
    coords = county_bounds.coordinates().getInfo()[0]
    lon_center = sum([pt[0] for pt in coords]) / len(coords)
    lat_center = sum([pt[1] for pt in coords]) / len(coords)

    # Create map centered on selected county
    m = geemap.Map(center=[lat_center, lon_center], zoom=10, basemap="HYBRID")

    # Add county boundary
    boundary_style = {"color": "red", "fillColor": "00000000", "width": 3}
    m.addLayer(county_fc.style(**boundary_style), {}, f"{selected_county} Boundary")

    # Display
    m.to_streamlit(height=850,width="stretch")
