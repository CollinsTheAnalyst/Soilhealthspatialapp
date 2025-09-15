import streamlit as st
from sidebar import render_sidebar
from streamlit_option_menu import option_menu
import geemap.foliumap as geemap
import folium
import ee
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim
import pandas as pd
import altair as alt


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

# Soil datasets (ISDA Africa)
ph = ee.Image("ISDASOIL/Africa/v1/ph").select('mean_0_20').divide(10).rename('pH')
nitrogen = ee.Image("ISDASOIL/Africa/v1/nitrogen_total").select('mean_0_20').divide(100).exp().subtract(1).rename('N')
phosphorous = ee.Image("ISDASOIL/Africa/v1/phosphorus_extractable").select('mean_0_20').divide(10).exp().subtract(1).rename('P')
potassium = ee.Image("ISDASOIL/Africa/v1/potassium_extractable").select('mean_0_20').divide(10).exp().subtract(1).rename('K')
calcium = ee.Image("ISDASOIL/Africa/v1/calcium_extractable").select('mean_0_20').divide(10).exp().subtract(1).rename('Ca')
magnesium = ee.Image("ISDASOIL/Africa/v1/magnesium_extractable").select('mean_0_20').divide(10).exp().subtract(1).rename('Mg')
cec = ee.Image("ISDASOIL/Africa/v1/cation_exchange_capacity").select('mean_0_20').divide(10).exp().subtract(1).rename('CEC')
iron = ee.Image("ISDASOIL/Africa/v1/iron_extractable").select('mean_0_20').divide(10).exp().subtract(1).rename('Fe')
carbon = ee.Image("ISDASOIL/Africa/v1/carbon_organic").select('mean_0_20').divide(10).exp().subtract(1).rename('Carbon')
zinc = ee.Image("ISDASOIL/Africa/v1/zinc_extractable").select('mean_0_20').divide(10).exp().subtract(1).rename('Zn')

nutrient_ranges = {
    "pH": (6.0, 7.5),
    "N": (0.2, 0.5),
    "P": (10, 25),
    "K": (75, 300),
    "Ca": (400, 1000),
    "Mg": (1, 3),
    "CEC": (10, 25),
    "Fe": (2, 6),
    "Carbon": (1, 3),
    "Zn": (20, 100),
}

# Kenya counties
kenya_counties = ee.FeatureCollection("projects/ee-collinsmwiti98/assets/KenyaCounties")
county_names = kenya_counties.aggregate_array("COUNTY").distinct().getInfo()

# Streamlit Page Config
st.set_page_config(page_title="GeoAgri Dashboard", page_icon="🌱", layout="wide")
render_sidebar("Soil Nutrient")
st.title("Soil Map")

# Layout: Map and controls
col1, col2 = st.columns([4, 1], gap="medium")

# Nutrient dictionary + visualization parameters
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
    "Zn": zinc,
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
    "Zn": {"min": 20, "max": 100, "palette": ["#f7fbff", "#6baed6", "#08306b"]},
}

options = list(nutrient_dict.keys())

# Sidebar controls
with col2:
    st.write("Select Soil Nutrients:")
    selected_nutrients = st.multiselect("Select Soil Nutrient(s)", options, default=["pH"])
    lat, lon, point = None, None, None
    
    st.markdown(
        '<small>🔹 Click on the map to select a point and view nutrient values.</small>',
        unsafe_allow_html=True
    )

    

# Map setup
with col1:
    m = geemap.Map(center=[1.2921, 36.8219], zoom=6)

    basemaps = {
        "Google Maps": folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
            attr="Google", name="Google Maps", overlay=False, control=True,
        ),
        "Google Satellite": folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google", name="Google Satellite", overlay=False, control=True,
        ),
        "Google Hybrid": folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
            attr="Google", name="Google Hybrid", overlay=False, control=True,
        ),
        "Google Terrain": folium.TileLayer(
            tiles="https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
            attr="Google", name="Google Terrain", overlay=False, control=True,
        ),
    }

    for basemap in basemaps.values():
        basemap.add_to(m)

    folium.LayerControl().add_to(m)

    if lat and lon:
        folium.Marker(
            location=[lat, lon],
            popup="Selected Point",
            icon=folium.Icon(color="blue", icon="map-marker")
        ).add_to(m)

    map_data = st_folium(m, height=700, width="stretch")

# Process clicks
# Process clicks
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]
    point = ee.Geometry.Point([lon, lat])

    # Get location name
    place_name = get_location_name(lat, lon)

    with col1:  # 👈 Ensure table + header appear in col1
        st.subheader(f"Soil Nutrient Values at {place_name} ({lat:.4f}, {lon:.4f})")

        # Collect results
        results = []
        for nut in selected_nutrients:
            result = nutrient_dict[nut].reduceRegion(
                reducer=ee.Reducer.mean(),
                geometry=point,
                scale=20
            ).getInfo()
            
            value = result.get(nut, None)

            if value is not None:
                min_val, max_val = nutrient_ranges.get(nut, (None, None))
                if min_val is not None and max_val is not None:
                    if value < min_val:
                        status = "🔴 Low"
                    elif value > max_val:
                        status = "🟠 High"
                    else:
                        status = "🟢 Within Range"
                    range_text = f"{min_val} - {max_val}"
                else:
                    status, range_text = "N/A", "N/A"

                results.append({
                    "Nutrient": nut,
                    "Value": round(value, 2),
                    "Recommended Range": range_text,
                    "Status": status
                })
            else:
                results.append({
                    "Nutrient": nut,
                    "Value": "No data",
                    "Recommended Range": "N/A",
                    "Status": "N/A"
                })

        df = pd.DataFrame(results)

        # ✅ Styled table
        st.data_editor(
            df,
            use_container_width=True,
            column_config={
                "Status": st.column_config.TextColumn(
                    "Status",
                    help="Shows whether the nutrient value is within the recommended range",
                ),
                "Value": st.column_config.NumberColumn(
                    "Value",
                    format="%.2f",
                ),
            },
            hide_index=True,
            disabled=True
        )

        # ✅ Altair chart
        df_range = df.copy()
        df_range[["Range Min", "Range Max"]] = df_range["Recommended Range"].str.split(" - ", expand=True)
        df_range["Range Min"] = pd.to_numeric(df_range["Range Min"], errors="coerce")
        df_range["Range Max"] = pd.to_numeric(df_range["Range Max"], errors="coerce")

        bars = alt.Chart(df_range).mark_bar(size=30).encode(
            x=alt.X("Value:Q", title="Measured Value"),
            y=alt.Y("Nutrient:N", sort="-x"),
            color=alt.Color("Status:N",
                            scale=alt.Scale(
                                domain=["🔴 Low", "🟢 Within Range", "🟠 High"],
                                range=["red", "green", "orange"]
                            )),
            tooltip=["Nutrient", "Value", "Recommended Range", "Status"]
        )

        ranges = alt.Chart(df_range).mark_rule(strokeDash=[4, 2], strokeWidth=2).encode(
            x="Range Min:Q",
            x2="Range Max:Q",
            y="Nutrient:N",
            tooltip=["Recommended Range"]
        )

        chart = (bars + ranges).properties(
            width=500,
            height=500,
            title="Soil Nutrient Levels vs Recommended Ranges"
        )

        st.altair_chart(chart, use_container_width=True)

    with col2:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download Data as CSV",
            data=csv,
            file_name=f"Soil_Nutrients_{place_name.replace(' ', '_')}.csv",
            mime="text/csv",
        )