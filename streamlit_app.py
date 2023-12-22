import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import base64

st.set_page_config(page_title="Image Segmentation App")

FLASK_SERVER_URL = "http://127.0.0.1:5000/segment"

def get_segmented_image(response):
    img_bytes = BytesIO(response.content)
    return Image.open(img_bytes)

with st.container():
    st.header("Image Segmentation App")
    st.write("---")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        if st.button("Submit"):
            files = {'image': uploaded_file.getvalue()}
            response = requests.post(FLASK_SERVER_URL, files=files)

            segmented_image = get_segmented_image(response)
            st.image(segmented_image, caption='Segmented Image', use_column_width=True)