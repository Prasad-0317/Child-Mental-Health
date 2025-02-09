import streamlit as st
from PIL import Image

# Set up page configuration
st.set_page_config(page_title="Child Mental Health", layout="wide", page_icon="🧠")

# Function to preprocess images
def preprocess_image(image_path, size=(300, 300)):
    img = Image.open(image_path)
    img = img.resize(size)
    return img

# Header with a styled navigation bar
st.markdown(
    """
    <style>
        /* Navbar Styling */
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

        /* Quotes Section Styling */
        .quote-box {
            width: 100%;
            height: 180px;  /* Fixed height for uniformity */
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
        }

        .quote-text {
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            line-height: 1.4;
        }

        .quote-author {
            font-style: italic;
            font-size: 14px;
            margin-top: 8px;
        }
    </style>
     <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">

    <div class="nav-bar">
        <div>
            <a href="#" class="logo">Logo for Child Mental Health</a>
            <a href="">Dashboard</a>
            <a href="#">Model</a>
            <a href="#">Chatbot</a>
            <a href="">About Us</a>
            <a href="">Our Motivation</a>
        </div>
        <div>
             <a href="#"><i class="fa fa-search icon"></i>Search</a>
            <a href="#">English</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("Child Mental Health")

# Quotes section
st.header("Quotes for Child Mental Health")
#st.write("Below are some inspiring quotes related to child mental health.")

# Quotes in 3 equal-sized boxes
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
        <div class="quote-box" style="background-color:#FFDDC1;">
            <p class="quote-text" style="color:#FF5733;">🌞 "Children's mental health is just as important as their physical health and deserves the same quality of support." 🌱</p>
            <p class="quote-author" style="color:#A52A2A;">- Kate Middleton</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="quote-box" style="background-color:#C1FFD7;">
            <p class="quote-text" style="color:#28A745;">💖 "The greatest gifts you can give your children are the roots of responsibility and the wings of independence." 🚀</p>
            <p class="quote-author" style="color:#2E8B57;">- Denis Waitley</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="quote-box" style="background-color:#C1E1FF;">
            <p class="quote-text" style="color:#007BFF;">🌈 "A child’s mental health is the foundation of their future happiness and success." 😊</p>
            <p class="quote-author" style="color:#1E90FF;">- Jack Shonkoff</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Main content: Images section
st.header("Images on Hover")
#st.write("Below are placeholder images. Replace these with your actual images.")

col1, col2, col3 = st.columns(3)
with col1:
    st.image(preprocess_image("img1.jpg"), caption="Image 1", use_column_width=True)
with col2:
    st.image(preprocess_image("img2.png"), caption="Image 2", use_column_width=True)
with col3:
    st.image(preprocess_image("img3.png"), caption="Image 3", use_column_width=True)

# Footer with contact info
st.markdown(
    """
    <hr>
    <div style="display: flex; justify-content: space-between; font-family: Arial, sans-serif; font-size: 14px;">
        <div>
            <h5>Terms and Conditions</h5>
            <p>[Placeholder for Terms and Conditions]</p>
        </div>
        <div>
            <h5>Child Mental Health</h5>
            <p>Mumbai, India</p>
            <p>+91 (734) 682 52</p>
        </div>
        <div>
            <h5>Get More Information</h5>
            <p>[Placeholder for additional information links]</p>
        </div>
    </div>
    <div class="footer">
        &copy; Copyright 2025 Child Mental Health, Inc
    </div>
    """,
    unsafe_allow_html=True,
)
