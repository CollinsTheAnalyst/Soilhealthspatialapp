
import streamlit as st
from sidebar import render_sidebar
from streamlit_option_menu import option_menu

# Set page configuration
st.set_page_config(page_title="Plant Disease Detection", page_icon="🌱", layout="wide")

render_sidebar("Plant Disease")

st.title ("Plant Disease Detection")