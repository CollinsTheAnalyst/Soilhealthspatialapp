import streamlit as st
import geemap
import ee
import pandas as pd

# Initialize Earth Engine
ee.Initialize(project="ee-collinsmwiti98")

# Page setup
st.set_page_config(page_title="NDVI Viewer", page_icon="🌱", layout="wide")
st.title("🌱 NDVI/EVI Analysis")

# Load farmer dataset
farmer_data = ee.FeatureCollection("projects/ee-collinsmwiti98/assets/homabayfarms")
farmer_names = farmer_data.aggregate_array("Farmer").distinct().getInfo()

# Sidebar inputs
col1, col2 = st.columns([4, 1])

with col2:
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

# Function to generate time series
def generate_time_series(farm_geom, metric, start, end):
    collection = (
        ee.ImageCollection("MODIS/006/MOD13Q1")
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
    if plot_button:
        df = generate_time_series(farm_geometry, metric, start_date, end_date)

        # Line chart
        st.line_chart(data=df, x='date', y='value', height=400, use_container_width=True)

        # CSV download
        if download_button:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f'{selected_farmer}_{metric}_timeseries.csv',
                mime='text/csv',
            )

    # Map display
    Map = geemap.Map(center=[0, 0], zoom=10)
    Map.addLayer(farm_geometry, {'color': 'yellow'}, "Selected Farm")
    Map.to_streamlit(height=400)
