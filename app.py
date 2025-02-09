import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Child Mental Health", layout="wide")

# Header with navigation bar
st.markdown(
    """
    <style>
        .nav-bar {
            display: flex;
            justify-content: space-between;
            background-color: #f0f0f0;
            padding: 10px 20px;
            font-family: Arial, sans-serif;
            font-size: 16px;
        }
        .nav-bar a {
            text-decoration: none;
            color: #333;
            padding: 0 15px;
        }
        .nav-bar a:hover {
            color: #007BFF;
        }
        .footer {
            text-align: center;
            font-size: 14px;
            margin-top: 20px;
            color: #555;
        }
    </style>
    <div class="nav-bar">
        <div>
            <a href="#">Logo for Child Mental Health</a>
            <a href="http://localhost:8502">Dashboard</a>
            <a href="#">Model</a>
            <a href="#">Chatbot</a>
            <a href="#">About Us</a>
            <a href="#">Our Motivation</a>
        </div>
        <div>
            <a href="#">Search</a>
            <a href="#">English</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("Child Mental Health")

# Main content: Images and Quotes section
st.header("Images on Hover")
st.write("Below are placeholder images. Replace these with your actual images.")

# Display images as placeholders
col1, col2, col3 = st.columns(3)
with col1:
    st.image("img1.jpg", caption="Image 1", use_column_width=True)
with col2:
    st.image("img2.png", caption="Image 2", use_column_width=True)
with col3:
    st.image("img3.png", caption="Image 3", use_column_width=True)

# Quotes section
st.header("Quotes for Mental Health")
st.write(
    """
    *"Half of all mental health conditions start in childhood, 
    but most cases go undetected and untreated."*
    """
)

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
