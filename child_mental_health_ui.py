import streamlit as st
import logging

# Set up logging
logging.basicConfig(filename='child_mental_health_app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set page configuration
st.set_page_config(page_title="Child Mental Health", layout="wide", initial_sidebar_state="expanded")

# Style using CSS
st.markdown("""
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f7f9fc;
        }
        .hover-img:hover {
            transform: scale(1.05);
            transition: transform 0.3s ease-in-out;
        }
        .quote-box {
            background-color: #e8f4f8;
            border-radius: 10px;
            padding: 20px;
            margin: 20px 0;
            font-size: 1.2em;
            color: #555;
            text-align: center;
            font-style: italic;
        }
        footer {
            text-align: center;
            margin-top: 20px;
            font-size: 0.9em;
            color: #777;
        }
    </style>
""", unsafe_allow_html=True)

# Header Section
col1, col2 = st.columns([1, 3])
with col1:
    st.image("C:\Users\devyaansh razdan\OneDrive\Desktop\Streamlit\logo.jpg", width=100)  # Replace with your logo image path
    logging.info("Logo displayed")
with col2:  
    st.title("Child Mental Health Awareness")
    logging.info("Title displayed")

# Search Bar
search_query = st.text_input("Search topics here", placeholder="Search...")
logging.info(f"Search query entered: {search_query}")

# Navigation Menu
nav_buttons = ["Dashboard", "Model", "Chatbot", "About Us", "Our Motivation"]
selected_page = st.radio("Choose a page", nav_buttons, horizontal=True)
logging.info(f"Page selected: {selected_page}")

# Main Page Content
if selected_page == "Dashboard":
    st.header("Dashboard Space")
    st.write("Explore insights and data related to child mental health.")
elif selected_page == "Model":
    st.header("Model")
    st.write("Learn about the models and analysis used to better understand child mental health.")
elif selected_page == "Chatbot":
    st.header("Chatbot")
    st.write("Interact with our chatbot to get quick help and guidance.")
elif selected_page == "About Us":
    st.header("About Us")
    st.write("Discover the mission, vision, and team behind this initiative.")
elif selected_page == "Our Motivation":
    st.header("Our Motivation")
    st.write("Understand the inspiration behind creating this platform.")

# Images with Awareness Messages
st.subheader("Child Mental Health Awareness")
col1, col2, col3 = st.columns(3)
with col1:
    st.image("C:\Users\devyaansh razdan\OneDrive\Desktop\Streamlit\img1.webp", use_column_width=True, caption="Empower through Awareness")  # Replace with your image
with col2:
    st.image("C:\Users\devyaansh razdan\OneDrive\Desktop\Streamlit\img2.png", use_column_width=True, caption="Support is Key")  # Replace with your image
with col3:
    st.image("C:\Users\devyaansh razdan\OneDrive\Desktop\Streamlit\img3.png", use_column_width=True, caption="Together We Can")  # Replace with your image

# Quote Section
st.subheader("Mental Health Awareness Quote")
st.markdown('<div class="quote-box">"The mind is not a vessel to be filled but a fire to be kindled."</div>', unsafe_allow_html=True)

# Footer Section
st.markdown("---")
st.markdown("""
<footer>
    <p>Terms and Conditions | Contact Us | Copyright Claim | Get More Info</p>
    <p>© 2025 Child Mental Health Awareness. All Rights Reserved.</p>
</footer>
""", unsafe_allow_html=True)
logging.info("Footer displayed")
