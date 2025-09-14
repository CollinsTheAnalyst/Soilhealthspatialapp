import streamlit as st
from sidebar import render_sidebar
import geemap
import ee
import pandas as pd
import geemap.foliumap as geemap
import folium
import altair as alt

# Initialize Earth Engine
ee.Initialize(project="ee-collinsmwiti98")

# Page setup
st.set_page_config(page_title="NDVI Viewer", page_icon="🌱", layout="wide")

render_sidebar("NDVI")

st.title("🌱 NDVI/EVI Analysis")

# Load farmer dataset
farmer_data = ee.FeatureCollection("projects/ee-collinsmwiti98/assets/homabayfarms")
farmer_names = farmer_data.aggregate_array("Farmer").distinct().getInfo()
kenya_counties = ee.FeatureCollection("projects/ee-collinsmwiti98/assets/KenyaCounties")
county_names = kenya_counties.aggregate_array("COUNTY").distinct().getInfo()

# Sidebar inputs
col1, col2 = st.columns([4, 1])

with col2:
    selected_county = st.selectbox("Select County", county_names)
    selected_farmer = st.selectbox("Select Farmer", farmer_names)
    metric = st.selectbox("Select Vegetation Index", ["NDVI", "EVI"], index=0)
    start_date = st.date_input("Start Date", value=pd.to_datetime("2000-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime("2024-12-31"))
    plot_button = st.button("📈 Plot Time Series")
    download_button = st.button("⬇ Download CSV")

# Filter selected farm
selected_farm_fc = farmer_data.filter(ee.Filter.eq("Farmer", selected_farmer))
farm_feature = selected_farm_fc.first()
farm_geometry = farm_feature.geometry()

#Filter county for map centering
selected_county_fc = kenya_counties.filter(ee.Filter.eq("COUNTY", selected_county))
county_feature = selected_county_fc.first()
county_geometry = county_feature.geometry()

# Function to generate time series
def generate_time_series(farm_geom, metric, start, end):
    collection = (
        ee.ImageCollection("MODIS/061/MOD13Q1")
        .filterBounds(farm_geom)
        .filterDate(str(start), str(end))
        .select([metric])
        .map(lambda img: img.multiply(0.0001).copyProperties(img, ['system:time_start']))
    )

    def extract_date_value(img):
        date = ee.Date(img.get('system:time_start')).format('YYYY-MM-dd')
        mean = img.reduceRegion(
            reducer=ee.Reducer.mean(),
            geometry=farm_geom,
            scale=250,
            bestEffort=True
        ).get(metric)
        return ee.Feature(None, {'date': date, 'value': mean})

    ts_fc = collection.map(extract_date_value)
    ts_list = ts_fc.toList(ts_fc.size()).getInfo()

    df = pd.DataFrame([f['properties'] for f in ts_list])
    df['date'] = pd.to_datetime(df['date'])
    return df.sort_values('date')


# Main display
with col1:
    # Create map
    Map = geemap.Map(center=[0, 0], zoom=4)
    Map.addLayer(selected_county_fc, {"color": "blue"}, selected_county)
    Map.centerObject(selected_county_fc, zoom=10)

    # Define custom basemaps (just like in Colab)
    basemaps = {
    "Google Maps": folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Maps",
        overlay=False,
        control=True,
    ),
    "Google Satellite": folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Satellite",
        overlay=False,
        control=True,
    ),
    "Google Hybrid": folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Hybrid",
        overlay=False,
        control=True,
    ),
    "Google Terrain": folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Terrain",
        overlay=False,
        control=True,
    ),
}

# Add them to the map
    for basemap in basemaps.values():
        basemap.add_to(Map)

# Add layer control (like in Colab)
    folium.LayerControl().add_to(Map)

# Show in Streamlit
    Map.to_streamlit(height=600)


if plot_button:
        df = generate_time_series(farm_geometry, metric, start_date, end_date)

        # Plot NDVI/EVI time series using Altair
if plot_button:
    df = generate_time_series(farm_geometry, metric, start_date, end_date)

    # Format start and end as Year-Month
    start_str = start_date.strftime("%Y-%m")
    end_str = end_date.strftime("%Y-%m")

    if not df.empty:
        chart_title = f"{selected_farmer} - {selected_county} {metric} Time Series ({start_str} to {end_str})"

        chart = (
            alt.Chart(df)
            .mark_line(point=True)
            .encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("value:Q", title=metric, scale=alt.Scale(zero=False)),
                tooltip=[alt.Tooltip("date:T", title="Date"),
                         alt.Tooltip("value:Q", title=metric)]
            )
            .properties(
                title=chart_title,
                height=400
            )
        )

        with col1:
            st.altair_chart(chart, use_container_width=True)

        # CSV download
        if download_button:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f'{selected_farmer}_{metric}_timeseries.csv',
                mime='text/csv',
            )