import streamlit as st
from PIL import Image

# Set up page configuration
st.set_page_config(page_title="Child Mental Health", layout="wide")

# Preprocess Images: Resize to uniform dimensions
def preprocess_image(image_path, size=(300, 300)):
    img = Image.open(image_path)
    img = img.resize(size)
    return img

# Header with a responsive and styled navigation bar
st.markdown(
    """
    <style>
        /* Import Font Awesome for icons */
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css');

        /* Navbar Styling */
        .nav-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #f8f9fa; /* Light gray background */
            padding: 10px 20px;
            border-radius: 10px; /* Curved edges */
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow */
            font-family: Arial, sans-serif;
            font-size: 16px;
        }

        .nav-bar div {
            display: flex;
            align-items: center;
        }

        .nav-bar a {
            text-decoration: none;
            color: #333;
            margin: 0 10px;
            display: flex;
            align-items: center;
            padding: 5px 10px;
            border-radius: 5px; /* Slight curve for links */
            transition: all 0.3s ease; /* Smooth hover effect */
        }

        .nav-bar a:hover {
            color: white;
            background-color: #007BFF; /* Blue hover effect */
        }

        /* Font Awesome search icon margin */
        .nav-bar .fa-search {
            margin-right: 5px;
        }

        /* Responsive Design for Navbar */
        @media (max-width: 768px) {
            .nav-bar {
                flex-direction: column;
                align-items: flex-start;
            }
            .nav-bar div {
                flex-direction: column;
                align-items: flex-start;
                margin-top: 10px;
            }
            .nav-bar a {
                margin: 5px 0; /* Stack links vertically on small screens */
            }
        }

        /* Quotes Section Styling */
        .quote-container {
            display: flex;
            justify-content: space-around; /* Even spacing between quotes */
            flex-wrap: wrap; /* Wrap quotes on smaller screens */
            gap: 20px; /* Add space between quotes */
            margin-top: 20px;
        }

        .quote-card {
            background: linear-gradient(135deg, #ff9a9e, #fad0c4); /* Gradient background */
            color: #fff; /* Text color */
            border-radius: 15px; /* Rounded corners */
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Slight shadow */
            padding: 20px;
            max-width: 280px; /* Limit width for uniformity */
            font-family: "Arial", sans-serif;
            text-align: center;
            font-size: 18px;
            line-height: 1.5;
            transition: transform 0.3s, box-shadow 0.3s; /* Smooth hover effect */
        }

        .quote-card:hover {
            transform: translateY(-8px); /* Lift effect on hover */
            box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.3); /* Darker shadow */
        }

        .quote-author {
            margin-top: 15px;
            font-size: 16px;
            font-style: italic;
            font-weight: bold;
            color: #f1f1f1; /* Lighter text for author */
        }

        /* Add different background colors for each card */
        .quote-card:nth-child(1) {
            background: linear-gradient(135deg, #6a11cb, #2575fc); /* Purple to blue */
        }

        .quote-card:nth-child(2) {
            background: linear-gradient(135deg, #ff9966, #ff5e62); /* Orange to red */
        }

        .quote-card:nth-child(3) {
            background: linear-gradient(135deg, #56ab2f, #a8e063); /* Green shades */
        }

        /* Styling for hover effect on images */
        .image-hover-container {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            gap: 20px;
        }

        .image-hover {
            transition: transform 0.3s ease, box-shadow 0.3s ease; /* Smooth transition */
            border-radius: 10px; /* Rounded corners */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Subtle shadow */
        }

        .image-hover:hover {
            transform: scale(1.1); /* Slight zoom effect on hover */
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); /* Enhanced shadow on hover */
        }
    </style>
    <div class="nav-bar">
        <div>
            <a href="#" class="logo">Logo for Child Mental Health</a>
            <a href="dashboard.py">Dashboard</a>
            <a href="#">Model</a>
            <a href="#">Chatbot</a>
            <a href="#">About Us</a>
            <a href="#">Our Motivation</a>
        </div>
        <div>
            <a href="#search">
                <i class="fas fa-search"></i> <!-- Font Awesome search icon -->
                Search
            </a>
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
st.write("Below are some inspiring and colorful quotes related to child mental health.")

# Colorful and visually appealing quotes section
st.markdown(
    """
    <div class="quote-container">
        <div class="quote-card">
            "Children's mental health is just as important as their physical health and deserves the same quality of support."
            <div class="quote-author">- Kate Middleton</div>
        </div>
        <div class="quote-card">
            "The greatest gifts you can give your children are the roots of responsibility and the wings of independence."
            <div class="quote-author">- Denis Waitley</div>
        </div>
        <div class="quote-card">
            "A child’s mental health is the foundation of their future happiness and success."
            <div class="quote-author">- Dr. Michael Carr-Gregg</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Images with hover effect
st.header("Images with Hover Effects")
st.write("Below are placeholder images with hover effects. Replace these with your actual images.")

# Display images with hover effects
st.markdown(
    """
    <div class="image-hover-container">
        <img src="img1.jpg" alt="Image 1" class="image-hover" width="300">
        <img src="img2.png" alt="Image 2" class="image-hover" width="300">
        <img src="img3.png" alt="Image 3" class="image-hover" width="300">
    </div>
    """,
    unsafe_allow_html=True,
)

# Footer with contact info
st.markdown(
    """
    <hr>
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; font-family: Arial, sans-serif; font-size: 14px;">
        <div style="flex: 1; min-width: 200px; padding: 10px;">
            <h5>Terms and Conditions</h5>
            <p>[Placeholder for Terms and Conditions]</p>
        </div>
        <div style="flex: 1; min-width: 200px; padding: 10px;">
            <h5>Child Mental Health</h5>
            <p>Mumbai, India</p>
            <p>+91 (734) 682 52</p>
        </div>
        <div style="flex: 1; min-width: 200px; padding: 10px;">
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
