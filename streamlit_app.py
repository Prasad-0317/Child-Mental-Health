
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
# Quotes Data
import streamlit as st
import time



# Quotes Data
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

# Initialize session state
if "quote_index" not in st.session_state:
    st.session_state.quote_index = 0

if "last_quote_time" not in st.session_state:
    st.session_state.last_quote_time = time.time()

# Display Quote
quote = quotes[st.session_state.quote_index]

st.markdown(
    f"""
    <div style="border-radius: 10px; padding: 20px; background-color: #f8f9fa; text-align: center;">
        <p style="color:{quote['color']}; font-size: 25px; font-weight: bold;">{quote['text']}</p>
        <p style="font-size: 16px; font-weight: bold; color: #555;font-size:25px"><i>— {quote['author']}</i></p>
    </div>
    """,
    unsafe_allow_html=True
)

# Navigation Buttons
col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("❮ Previous"):
        st.session_state.quote_index = (st.session_state.quote_index - 1) % len(quotes)
        st.session_state.last_quote_time = time.time()
        st.rerun()

with col3:
    if st.button("Next ❯"):
        st.session_state.quote_index = (st.session_state.quote_index + 1) % len(quotes)
        st.session_state.last_quote_time = time.time()
        st.rerun()

# **Auto-switch quote every 5 seconds**
if time.time() - st.session_state.last_quote_time >= 5:
    st.session_state.quote_index = (st.session_state.quote_index + 1) % len(quotes)
    st.session_state.last_quote_time = time.time()
    st.rerun()



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
  margin-left: 100px;

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

<div style="text-align:center;margin-block-start: -10px;margin-left: -100px;">
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

# ---------------------------------

import streamlit as st

# Initialize chatbot visibility state
if "chatbot_visible" not in st.session_state:
    st.session_state.chatbot_visible = False

# Chatbot HTML with proper positioning and no white background
chatbot_html = f"""
    <style>
        /* Floating Chat Button */
        .chatbot-button {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #007BFF;
            color: white;
            border: none;
            padding: 12px 18px;
            border-radius: 50px;
            cursor: pointer;
            font-size: 16px;
            box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.2);
            transition: background 0.3s;
            z-index: 1000;
        }}
        .chatbot-button:hover {{
            background: #0056b3;
        }}

        /* Chatbot Window (No White Background) */
        .chatbot-container {{
            position: fixed;
            bottom: 80px;
            right: 20px;
            width: 350px;
            height: 500px;
            background: transparent;
            border-radius: 10px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            overflow: hidden;
            z-index: 999;
            display: {"block" if st.session_state.chatbot_visible else "none"};
        }}

        /* Ensure iframe takes full space */
        .chatbot-container iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
    </style>

    <!-- Chat Button -->
    <button class="chatbot-button" onclick="toggleChatbot()">💬 Chat</button>

    <!-- Chatbot Window -->
    <div class="chatbot-container">
        <iframe src="http://127.0.0.1:5500/index.html"></iframe>
    </div>

    <script>
        function toggleChatbot() {{
            var chatbot = document.querySelector('.chatbot-container');
            chatbot.style.display = chatbot.style.display === "none" ? "block" : "none";
        }}
    </script>
"""

# Render chatbot in Streamlit
st.components.v1.html(chatbot_html, height=600, scrolling=False)







# -----------------

# import streamlit as st

# # Chatbot HTML with correct positioning and direct Dialogflow load
# chatbot_html = f"""
#     <style>
#         /* Floating Chat Button */
#         .chatbot-button {{
#             position: fixed;
#             bottom: 20px;
#             right: 20px;
#             background: #007BFF;
#             color: white;
#             border: none;
#             padding: 12px 18px;
#             border-radius: 50px;
#             cursor: pointer;
#             font-size: 16px;
#             box-shadow: 0px 3px 6px rgba(0, 0, 0, 0.2);
#             transition: background 0.3s;
#             z-index: 1000;
#         }}
#         .chatbot-button:hover {{
#             background: #0056b3;
#         }}

#         /* Chatbot Window */
#         .chatbot-container {{
#             position: fixed;
#             bottom: 80px;
#             right: 20px;
#             width: 350px;
#             height: 500px;
#             border-radius: 10px;
#             box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
#             overflow: hidden;
#             display: none;
#             z-index: 999;
#         }}

#         /* Ensure iframe takes full space */
#         .chatbot-container iframe {{
#             width: 100%;
#             height: 100%;
#             border: none;
#         }}
#     </style>

#     <!-- Chat Button -->
#     <button class="chatbot-button" onclick="toggleChatbot()">💬 Chat</button>

#     <!-- Chatbot Window (Loads Dialogflow Directly) -->
#     <div id="chatbot-box" class="chatbot-container">
#         <iframe src="https://console.dialogflow.com/api-client/demo/embedded/a21d644c-7b13-4be4-b8ba-f3880a95aa6e"></iframe>
#     </div>

#     <script>
#         function toggleChatbot() {{
#             var chatbotBox = document.getElementById('chatbot-box');
#             chatbotBox.style.display = chatbotBox.style.display === "none" ? "block" : "none";
#         }}
#     </script>
# """

# # Render chatbot in Streamlit
# st.components.v1.html(chatbot_html, height=600, scrolling=False)


# ------------------------------  chatbot 2 --------------------------

# import streamlit as st

# # Load the chatbot interface
# with open("index.html", "r", encoding="utf-8") as f:
#     html_content = f.read()

# st.components.v1.html(html_content, height=600, scrolling=True)

# # Injecting CSS for Dialogflow Chatbot positioning
# st.markdown(
#     """
#     <style>
#         df-messenger {
#             position: fixed;
#             bottom: 20px;
#             right: 20px;
#             z-index: 9999;
#             --df-messenger-bot-message: #007bff;
#             --df-messenger-user-message: #6c757d;
#             --df-messenger-input-box-color: #f1f1f1;
#             --df-messenger-font-color: white;
#             --df-messenger-input-font-color: black;
#         }

#         /* Ensure the floating button is correctly positioned */
#         df-messenger::part(toggle-button) {
#             position: fixed;
#             bottom: 20px;
#             right: 20px;
#             background-color: #007bff !important;
#             border-radius: 50%;
#             box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.3);
#         }
#     </style>
#     """,
#     unsafe_allow_html=True
# )







# -----------

st.markdown(
    """
    <style>
    .footer {
            position:fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            height:5%;
            background-color: #000;
            color: white;
            text-align: center;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            text-align: center;
            font-size: 16px;
            color: #fff;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
    </style>
    <div class="footer"; style="display: flex; justify-content: center; font-family: Arial, sans-serif; font-size: 14px;">
        &copy; Copyright 2025 Child Mental Health, India
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------








# ------------------
