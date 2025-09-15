import streamlit as st
from sidebar import render_sidebar
from streamlit_option_menu import option_menu
import pandas as pd

# Set page configuration
st.set_page_config(page_title="Fertilizer Reccomendation System", page_icon="🌱", layout="wide")

render_sidebar("Crop Nutrient Requirement")

st.title("Crop Nutrient Requirements")
