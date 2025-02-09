import streamlit as st
from PIL import Image

# Set up page configuration
st.set_page_config(page_title="Child Mental Health", layout="wide")

# Function to preprocess images
def preprocess_image(image_path, size=(200, 200)):
    img = Image.open(image_path)
    img = img.resize(size)
    return img

# Navigation Bar
st.markdown(
    """
    <style>
        .nav-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #f8f9fa;
            padding: 10px 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            font-family: Arial, sans-serif;
            font-size: 16px;
        }
        .nav-bar a {
            text-decoration: none;
            color: #333;
            margin: 0 10px;
            padding: 5px 10px;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        .nav-bar a:hover {
            color: white;
            background-color: #007BFF;
        }
    </style>
    <div class="nav-bar">
        <div>
            <a href="#" class="logo">Logo</a>
            <a href="#">Home</a>
            <a href="#">Model</a>
            <a href="#">Chatbot</a>
            <a href="#">About Us</a>
            <a href="#">Motivation</a>
        </div>
        <div>
            <a href="#">🔍 Search</a>
            <a href="#">English</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("Child Mental Health")

# Quotes Section
st.header("Inspiring Quotes")
col1, col2, col3 = st.columns(3)
with col1:
    st.info("🌞 \"Children's mental health is as important as their physical health.\" - Kate Middleton")
with col2:
    st.success("💖 \"The greatest gift to children is emotional security.\" - Denis Waitley")
with col3:
    st.warning("🌈 \"A child’s mental health is the foundation of their future happiness.\" - Jack Shonkoff")

# Image Carousel
st.header("Image Gallery")
image_paths = ["img1.jpg", "img2.png", "img3.png"]
if 'image_index' not in st.session_state:
    st.session_state.image_index = 0

def prev_image():
    st.session_state.image_index = (st.session_state.image_index - 1) % len(image_paths)

def next_image():
    st.session_state.image_index = (st.session_state.image_index + 1) % len(image_paths)

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("⬅ Previous"):
        prev_image()
with col2:
    st.image(preprocess_image(image_paths[st.session_state.image_index]), caption=f"Image {st.session_state.image_index + 1}", use_column_width=True)
with col3:
    if st.button("Next ➡"):
        next_image()

# Footer
st.markdown(
    """
    <hr>
    <div style="text-align: center; font-size: 14px;">
        &copy; 2025 Child Mental Health, Inc. | Terms & Conditions | Contact Us
    </div>
    """,
    unsafe_allow_html=True,
)
