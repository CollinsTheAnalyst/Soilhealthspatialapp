import streamlit as st

def render_sidebar(page_name: str):
    # --- Sidebar background color and text styling ---
    st.markdown(
        """
         <style>
        [data-testid="stSidebar"] {
            background-color: #1b4332;  /* Dark green */
            padding: 5px;
            border-radius: 15px;        /* Rounded corners */
            margin: 10px;               /* Space from window edge */
            width: 420px !important;    /* Shrink width */
            box-shadow: 2px 2px 12px rgba(0,0,0,0.3); /* Floating effect */
        }

        }
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #2e7d32; /* green titles */
            font-size: 1.25rem; /* bigger titles */
        }
        [data-testid="stSidebar"] p, 
        [data-testid="stSidebar"] li, 
        [data-testid="stSidebar"] div {
            font-size: 1.1rem; /* bigger normal text */
            line-height: 1.4;  /* improve readability */
            color: #ffffff;    /* white for normal text */
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --- Sidebar Content ---
    st.sidebar.image("logo2.png", width="stretch")

    st.sidebar.title("About")

    about_dict = {
        "Boundary Mapping": "This page helps visualize and manage farm boundaries using spatial datasets and drawing tools.",
        "Crop Nutrient Requirement": "This page calculates crop nutrient needs based on soil fertility and crop type.",
        "NDVI": "This page provides NDVI/EVI time series for monitoring vegetation health and crop growth.",
        "Plant Disease": "This page supports plant disease detection and management using field data and imagery.",
        "Soil Nutrient": "This page visualizes soil nutrient maps (pH, N, P, K, Ca, Mg, etc.) from ISDA Africa soil data.",
        "Soil Taxonomic Group": "This page classifies soils into taxonomic groups to aid in soil management planning.",
    }

    about_text = about_dict.get(
        page_name,
        "This is part of the GeoAgri Dashboard for soil and crop health analysis."
    )
    st.sidebar.info(about_text)

    st.sidebar.title("Contact")
    st.sidebar.info("""
    Collins Mwiti |  
    0714326105 |  
    Collinskimathimwiti@gmail.com |  
    [GitHub](https://github.com/CollinsTheAnalyst) |   
    [LinkedIn](https://www.linkedin.com/in/giswqs)
    """)
