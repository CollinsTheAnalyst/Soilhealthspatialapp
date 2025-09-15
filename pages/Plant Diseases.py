import streamlit as st
from sidebar import render_sidebar
from streamlit_option_menu import option_menu
import tensorflow as tf
import numpy as np

# Set page configuration
st.set_page_config(page_title="Plant Disease Detection", page_icon="🌱", layout="wide")

render_sidebar("Plant Disease")

st.title("🌱 Plant Disease Detection")

col1, col2 = st.columns([3,2], gap="small", border=True, vertical_alignment="top", width="stretch")

with col1:
    st.image("Data/home_page(1).jpeg", width="stretch")

    # --- Load model once (outside function for efficiency) ---
    @st.cache_resource
    def load_model():
        return tf.keras.models.load_model("trained_model.h5")

    model = load_model()

    # --- Prediction function ---
    def model_prediction(test_image):
        image = tf.keras.preprocessing.image.load_img(test_image, target_size=(128,128))
        image = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.array([image])  # Convert single image to a batch
        predictions = model.predict(input_arr)
        return np.argmax(predictions)  # Get index of highest probability

    # --- UI for uploading ---
    test_image = st.file_uploader("📂 Choose a leaf image for prediction", type=["jpg", "jpeg", "png"])

    if test_image is not None:
        st.image(test_image, caption="Uploaded Image", use_container_width=True)

        if st.button("🔍 Predict"):
            st.snow()
            result_index = model_prediction(test_image)

            # Class labels
            class_name = [
                'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
                'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 
                'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 
                'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 
                'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
                'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot',
                'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
                'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 
                'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
                'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 
                'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
                'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 
                'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus',
                'Tomato___healthy'
            ]

            st.success(f"✅ Model Prediction: **{class_name[result_index]}**")
