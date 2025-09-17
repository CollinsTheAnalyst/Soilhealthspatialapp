import streamlit as st
from sidebar import render_sidebar
import pandas as pd
from io import BytesIO

# Set page configuration
st.set_page_config(page_title="Fertilizer Recommendation System", page_icon="🌱", layout="wide")

render_sidebar("Crop Nutrient Requirement")

# Load crop nutrient data
cropdata = pd.read_csv("CropNutrientsdata - Sheet1.csv")

st.title("Crop Nutrient Requirements")
st.write("""This page provides a fertilizer recommendation system based on crop nutrient requirements.""")

# --- Input columns ---
col1, col2, col3, col4 = st.columns([1,1,1,1], gap="small")

with col1:
    selected_crop = st.selectbox("Select Crop", cropdata["Crop"].tolist())

with col2:
    size_unit = st.selectbox("Select Farm Size Unit", ["Hectares", "Acres"])

with col3:
    farm_size = st.number_input(f"Enter Farm Size ({size_unit})", min_value=0.1, step=0.1, value=1.0)

# --- Filter nutrient data for selected crop ---
selected_crop_data = cropdata[cropdata["Crop"] == selected_crop]

# --- Convert farm size to hectares ---
farm_size_ha = farm_size if size_unit == "Hectares" else farm_size * 0.404686

# --- Calculate total nutrient requirements ---
nutrient_scaled = selected_crop_data.copy()
nutrient_scaled["Total Nitrogen Required (kg)"] = (nutrient_scaled["Total Nitrogen Required(kg/ha)"] * farm_size_ha).round(0).astype(int)
nutrient_scaled["Total Phosphorus Required (kg)"] = (nutrient_scaled["Total Phosphorus Required(kg/ha)"] * farm_size_ha).round(0).astype(int)
nutrient_scaled["Total Potassium Required (kg)"] = (nutrient_scaled["Total Potassium Required(kg/ha)"] * farm_size_ha).round(0).astype(int)

# --- Reduce table width ---
st.markdown(
    """
    <style>
    .dataframe table {
        width: 60% !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Display nutrient table without index ---
st.subheader(f"Nutrient Requirements for {selected_crop} ({round(farm_size, 2)} {size_unit})")

st.dataframe(
    nutrient_scaled[[
        "Crop",
        "Total Nitrogen Required (kg)",
        "Total Phosphorus Required (kg)",
        "Total Potassium Required (kg)"
    ]],
    use_container_width=False
)

# --- Soil Test Inputs ---
st.subheader("Enter Soil Test Results (Optional)")

col_n, col_p, col_k, col_ph, col_ec, col6, col7 = st.columns(7, gap="small")

with col_n:
    soil_n = st.number_input("Soil Nitrogen (%)", min_value=0.0, step=0.01, format="%.2f")

with col_p:
    soil_p = st.number_input("Soil Phosphorus (ppm)", min_value=0.0, step=1.0)

with col_k:
    soil_k = st.number_input("Soil Potassium (ppm)", min_value=0.0, step=1.0)

with col_ph:
    soil_ph = st.number_input("Soil pH", min_value=0.0, max_value=14.0, step=0.1, format="%.2f")

with col_ec:
    soil_ec = st.number_input("Soil EC (dS/m)", min_value=0.0, step=0.01, format="%.2f")


# --- Fertilizer Selection by Stage ---
st.subheader("Fertilizer Application Stage")

# Stage selection: Planting or Top Dressing
stage = st.radio("Select Crop Stage", ["Planting", "Top Dressing"])

# Fertilizers available per stage
planting_ferts = ["DAP", "TSP", "SSP", "NPK 20-10-10"]
topdress_ferts = ["CAN", "Urea", "NPK 46-0-0"]

# User selects fertilizer based on stage
if stage == "Planting":
    selected_fert = st.selectbox("Select Fertilizer for Planting", planting_ferts)
else:
    selected_fert = st.selectbox("Select Fertilizer for Top Dressing", topdress_ferts)

# --- Fertilizer nutrient content lookup (example %) ---
fert_nutrients = {
    "DAP": {"N": 18, "P": 46, "K": 0},
    "TSP": {"N": 0, "P": 46, "K": 0},
    "SSP": {"N": 0, "P": 16, "K": 0},
    "NPK 20-10-10": {"N": 20, "P": 10, "K": 10},
    "CAN": {"N": 26, "P": 0, "K": 0},
    "Urea": {"N": 46, "P": 0, "K": 0},
    "NPK 46-0-0": {"N": 46, "P": 0, "K": 0},
}

# --- Mock calculation based on stage ---
N_req = nutrient_scaled["Total Nitrogen Required (kg)"].values[0]
P_req = nutrient_scaled["Total Phosphorus Required (kg)"].values[0]
K_req = nutrient_scaled["Total Potassium Required (kg)"].values[0]

fert = fert_nutrients[selected_fert]

if stage == "Planting":
    # P 100% applied
    fert_p_needed = P_req / (fert["P"]/100) if fert["P"] > 0 else 0
    # K 50% applied
    fert_k_needed = (0.5*K_req) / (fert["K"]/100) if fert["K"] > 0 else 0
    # N supplied by fertilizer
    N_supplied = fert["N"]/100 * (fert_p_needed if fert_p_needed > 0 else 0)
    N_remaining = N_req - N_supplied

    st.write(f"Fertilizer to apply at Planting: {round(fert_p_needed + fert_k_needed,2)} kg")
    st.write(f"N supplied: {round(N_supplied,2)} kg, N remaining for top dressing: {round(N_remaining,2)} kg")

else:
    # Top dressing uses remaining N and remaining K
    fert_n_needed = N_req / (fert["N"]/100) if fert["N"] > 0 else 0
    fert_k_needed = (0.5*K_req) / (fert["K"]/100) if fert["K"] > 0 else 0

    st.write(f"Fertilizer to apply at Top Dressing: {round(fert_n_needed + fert_k_needed,2)} kg")


