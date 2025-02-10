
import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import time

st.set_page_config(page_title="Child Mental Health", layout="wide", page_icon="🧠")

# Apply custom styling to prevent overlap
st.markdown(
    """
    <style>
        .main-content {
            padding-left: 35px; /* Adjust to shift content when sidebar is collapsed */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Main content container with padding
with st.container():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    st.logo("logo - Copy.jpg", size="medium")
    # st.title("Child Mental Health ..")
    # with open("index.html", "r", encoding="utf-8") as f:
    #     html_content = f.read()


    # st.components.v1.html(html_content, height=600, scrolling=True)
    # st.markdown('</div>', unsafe_allow_html=True)



# Sidebar Navigation
with st.sidebar:
    st.page_link("streamlit_app.py", label="Home", icon=":material/home:")
    st.page_link("http://localhost:8503/", label="About Us", icon=":material/groups:")
    st.page_link("http://localhost:8503/", label="Our Motivation", icon=":material/workspace_premium:")
    st.page_link("http://localhost:8504/", label="Model", icon=":material/network_intelligence_update:")
    st.page_link("http://localhost:8502/", label="Dashboard", icon=":material/dashboard:")
    st.page_link("http://localhost:8504/", label="Chatbot", icon=":material/forum:")
    st.page_link("http://localhost:8504/", label="Feedback", icon=":material/mood:")




container_style = """
        <style>
        .stApp {
            background-color:;
        }
        [alt=Logo] {
            height: 8rem;
            width: 8rem;
            border-radius: 20%;
            object-fit: fill;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            border: 2px solid #007BFF;
        }
        #child-mental-health{
            font-weight:400;
            font-size:40px;
            inline-size:auto
        }
        .st-emotion-cache-1104ytp h1{
            padding:2.25rem 0px 1rem;
        }
        div.chat-wrapper {
            position: relative;
            z-index: 1; /* Ensure it doesn't overlap the chatbot icon */
        }
        .stApp > div {
            overflow: visible !important;
        }
        
          .st-emotion-cache-1y4p8pa {
            padding: 10px 15px;
            border-radius: 5px;
            transition: background-color 0.3s, color 0.3s;
        }
        
        /* Hover effect */
        .st-emotion-cache-1y4p8pa:hover {
            background-color: #122f8e !important;
            color: #dcdebc !important;
            cursor: pointer;
            font-weight: bold;
        }
        
        /* Active link style */
        .st-emotion-cache-1y4p8pa:active {
            background-color: #0b1c5c !important;
            color: white !important;
        }

        </style>
    """
st.markdown(container_style, unsafe_allow_html=True)

# # Quotes section
# st.header("Quotes for Child Mental Health")

# List of quotes
quotes = [
    {
        "text": "🌞 Children's mental health is just as important as their physical health and deserves the same quality of support. 🌱",
        "author": "Kate Middleton",
        "color": "#FF5733"
    },
    {
        "text": "💖 The greatest gifts you can give your children are the roots of responsibility and the wings of independence. 🚀",
        "author": "Denis Waitley",
        "color": "#28A745"
    },
    {
        "text": "🌈 A child’s mental health is the foundation of their future happiness and success. 😊",
        "author": "Jack Shonkoff",
        "color": "#007BFF"
    }
]

# Initialize session state for quote index
if 'quote_index' not in st.session_state:
    st.session_state.quote_index = 0

# Function to update quote index
def update_quote_index(delta):
    st.session_state.quote_index = (st.session_state.quote_index + delta) % len(quotes)

# Display quote with navigation buttons
quote = quotes[st.session_state.quote_index]
st.markdown(
    f"""
    <div class="quote-container">
        <div class="quote-text" style="color:{quote['color']};">{quote['text']}</div>
        <div class="quote-author">- {quote['author']}</div>
        <div class="quote-navigation">
            <button onclick="updateQuote(-1)">❮</button>
            <button onclick="updateQuote(1)">❯</button>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# JavaScript for quote navigation
st.markdown(
    """
    <script>
        function updateQuote(delta) {
            fetch(/update_quote?delta=${delta}, { method: 'GET' })
                .then(() => window.location.reload());
        }
    </script>
    """,
    unsafe_allow_html=True,
)

# Streamlit endpoint to update quote index
if st.experimental_get_query_params().get("delta"):
    delta = int(st.experimental_get_query_params()["delta"][0])
    update_quote_index(delta)

# Automatically change quotes every 5 seconds
if "last_quote_change" not in st.session_state:
    st.session_state.last_quote_change = time.time()

if time.time() - st.session_state.last_quote_change > 5:  # Change quote every 5 seconds
    update_quote_index(1)
    st.session_state.last_quote_change = time.time()

# -------------

import streamlit.components.v1 as components

components.html(
    """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {box-sizing: border-box;}
body {font-family: Verdana, sans-serif;}
.mySlides {display: none;}
img {vertical-align: middle;}

/* Slideshow container */
.slideshow-container {
  max-width: 1000px;
  position: relative;
  margin-left: auto;

}

/* Caption text */
.text {
  color: #f2f2f2;
  font-size: 15px;
  padding: 8px 12px;
  position: absolute;
  bottom: 8px;
  width: 100%;
  text-align: center;
}

/* Number text (1/3 etc) */
.numbertext {
  color: #f2f2f2;
  font-size: 12px;
  padding: 8px 12px;
  position: absolute;
  top: 0;
}

/* The dots/bullets/indicators */
.dot {
  height: 10px;
  width: 10px;
  margin: 0 0.5px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
  transition: background-color 0.6s ease;
  margin-left: 32px;
}

.active {
  background-color: #717171;
}

/* Fading animation */
.fade {
  animation-name: fade;
  animation-duration: 5s;
}

@keyframes fade {
  from {opacity: .4} 
  to {opacity: 1}
}

/* On smaller screens, decrease text size */
@media only screen and (max-width: 300px) {
  .text {font-size: 11px}
}

</style>
</head>
<body>

<h2></h2>


<div class="slideshow-container">

<div class="mySlides fade">
  <div class="numbertext">1 / 4</div>
  <img src="https://www.mpowerminds.com/assetOLD/images/psychiatrist_in_mumbaisd.jpg" style="width:80%; height:70vh;width:100vh">
  <div class="text"></div>
</div>

<div class="mySlides fade">
  <div class="numbertext">2 / 4</div>
  <img src="https://domf5oio6qrcr.cloudfront.net/medialibrary/14528/3f85b1b1-9dc7-4a90-855c-dc204646e889.jpg" style="width:100%; height:70vh;width:100vh">
  <div class="text"></div>
</div>

<div class="mySlides fade">
  <div class="numbertext">3 / 4</div>
  <img src="https://eskimo3.ie/wp-content/uploads/2023/02/36.-mental-health.jpg" style="width:100%; height:70vh;width:100vh">
  <div class="text"></div>
</div>
<div class="mySlides fade">
  <div class="numbertext">4 / 4</div>
  <img src="https://kickstarterz.co.uk/wp-content/uploads/2021/02/children-and-mental-health.png" style="width:100%; height:70vh;width:100vh">
  <div class="text"></div>
</div>

</div>
<br>

<div style="text-align:center;margin-block-start: -10px;margin-left: -200px;">
  <span class="dot"></span> 
  <span class="dot"></span> 
  <span class="dot"></span>
  <span class="dot"></span>
</div>

<script>
let slideIndex = 0;
showSlides();

function showSlides() {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
  for (i = 0; i < slides.length; i++) {
    slides[i].style.display = "none";  
  }
  slideIndex++;
  if (slideIndex > slides.length) {slideIndex = 1}    
  for (i = 0; i < dots.length; i++) {
    dots[i].className = dots[i].className.replace(" active", "");
  }
  slides[slideIndex-1].style.display = "block";  
  dots[slideIndex-1].className += " active";
  setTimeout(showSlides, 5000); // Change image every 2 seconds
}
</script>

</body>
</html> 

    """,
    height=600
)



# -----------



# Footer with contact info
st.markdown(
    """
    <style>
    .footer {
            # position:fixed;
            margin-top: 40px;
            padding: 20px;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            text-align: center;
            font-size: 16px;
            color: #fff;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
    </style>
    <div class="footer"; style="display: flex; justify-content: center; font-family: Arial, sans-serif; font-size: 14px;">
        &copy; Copyright 2025 Child Mental Health, Inc
    </div>
    """,
    unsafe_allow_html=True,
)
