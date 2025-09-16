import streamlit as st
from sidebar import render_sidebar
from streamlit_option_menu import option_menu
import geemap
import geemap.foliumap as geemap
import ee
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import st_folium
from legend import soil_code_guide


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

# Load styled soils (exported version with colors)
kenya_soils = ee.FeatureCollection("projects/ee-collinsmwiti98/assets/kenyasoils_styled")

st.title("Soil Taxonomic Groups")
col1, col2 = st.columns([4,1], gap="medium")

with col2:
    selected_county = st.selectbox("Select County", county_names)
    county_fc = kenya_counties.filter(ee.Filter.eq("COUNTY", selected_county))

    st.info("Please select a point on the map to view detailed soil data for the location.")

with col1:
    # Center map on selected county
    county_bounds = county_fc.geometry().bounds()
    coords = county_bounds.coordinates().getInfo()[0]
    lon_center = sum([pt[0] for pt in coords]) / len(coords)
    lat_center = sum([pt[1] for pt in coords]) / len(coords)

    # Initialize map with basemap
    m = geemap.Map(center=[lat_center, lon_center], zoom=8, basemap="HYBRID")


    # Add county boundary
    boundary_style = {"color": "red", "fillColor": "#00000000", "width": 3}  # transparent fill
    m.addLayer(county_fc.style(**boundary_style), {}, f"{selected_county} Boundary")

    # Clip already styled soils to the selected county
    county_soils = ee.FeatureCollection("projects/ee-collinsmwiti98/assets/kenyasoils_styled").filterBounds(county_fc)

    # Add the styled soils layer directly
    m.addLayer(county_soils, {}, "Soil Taxonomic Groups")

    # Display map in Streamlit
    map_data = st_folium(m, height=600, width="stretch")

    soil_types = county_soils.aggregate_array("DOMSOI").distinct().getInfo()
    full_names = [soil_code_guide.get(code, code) for code in soil_types]

    st.subheader(f"Soil types in {selected_county}")
    st.write(", ".join(full_names))

    # --- Handle click (if point drawn) ---
    if map_data and map_data.get("last_clicked"):
        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]
                
        clicked_point = ee.Geometry.Point(lon, lat)

        # Find soil polygon containing the point
        selected_soil = county_soils.filterBounds(clicked_point).first()

        if selected_soil:
            soil_at_point = county_soils.filterBounds(clicked_point).first().get('DOMSOI').getInfo()
            full_name = soil_code_guide.get(soil_at_point, soil_at_point)


            location_name = get_location_name(lat, lon)

            st.success(f"📍 Location: {location_name}")
            st.write(f"**Soil Code:** {soil_at_point}")
            st.write(f"**Soil Type:** {full_name}")

