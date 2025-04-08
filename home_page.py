import streamlit as st
from streamlit_option_menu import option_menu
from PIL import Image
import time
import streamlit.components.v1 as components
import random

# Configure page settings
st.set_page_config(page_title="Child Mental Health", layout="wide", page_icon="🧠")

# Main background and styling
st.markdown("""
<style>
    /* Apply background to the entire app */
    .stApp {
        background-image: url('https://img.freepik.com/free-vector/hand-painted-watercolor-pastel-sky-background_23-2148902771.jpg');
        background-size: cover;
        background-position: center;
        min-height: 100vh;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    @keyframes rainbow {
        0% { color: #ff73a1; }
        25% { color: #ffaa5b; }
        50% { color: #7fdeff; }
        75% { color: #9f7fef; }
        100% { color: #ff73a1; }
    }
    
    .rainbow-text {
        font-size: 42px;
        font-weight: 600;
        animation: rainbow 8s infinite;
        -webkit-text-stroke: 1.5px black; /* Black outline for Webkit browsers */
        text-stroke: 1.5px black; /* Standard syntax (less supported) */
        paint-order: stroke fill; /* Ensures stroke is drawn before fill */
    }
    
    .floating {
        animation: float 4s ease-in-out infinite;
        display: inline-block;
    }

    /* Styling for intro text */
    .intro-text {
        font-size: 18px;
        line-height: 1.6;
        margin-bottom: 20px;
        background: rgba(255, 255, 255, 0.85);
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        color: #333;
        font-weight: 500;
        border-left: 5px solid #6a11cb;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .intro-text:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
    }
    
    .sidebar .sidebar-content {
        background-image: linear-gradient(180deg, #a1c4fd 0%, #c2e9fb 100%);
        border-radius: 15px;
    }
    
    [alt=Logo] {
        height: 8rem;
        width: 8rem;
        border-radius: 20%;
        object-fit: fill;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
        border: 3px solid #6a11cb;
        transition: transform 0.3s;
    }
    
    [alt=Logo]:hover {
        transform: scale(1.05);
    }
    
    .quote-container {
        border-radius: 15px;
        padding: 20px;
        background: rgba(255, 255, 255, 0.8);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        border-left: 5px solid #6a11cb;
        transition: transform 0.3s;
    }
    
    .quote-container:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    /* Enhanced Navigation Styling with Increased Specificity */
    [data-testid="stSidebar"] .nav-link, 
    [data-testid="stSidebar"] a {
        padding: 12px 20px !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border-left: 5px solid transparent !important;
        transition: all 0.3s ease-in-out !important;
        position: relative !important;
        overflow: hidden !important;
        font-weight: 500 !important;
        color: #333 !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
        display: block !important;
        text-decoration: none !important;
        z-index: 1 !important;
    }

    [data-testid="stSidebar"] .nav-link:hover, 
    [data-testid="stSidebar"] a:hover {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%) !important;
        color: #ffffff !important; /* White text on hover */
        border-left: 5px solid #fff !important;
        transform: translateX(8px) scale(1.02) !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2) !important;
        -webkit-text-fill-color: #ffffff !important; /* Ensure text fill is white */
        text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important; /* Subtle shadow for better contrast */
    }

    [data-testid="stSidebar"] .nav-link::before, 
    [data-testid="stSidebar"] a::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease;
        z-index: 0;
    }

    [data-testid="stSidebar"] .nav-link:hover::before, 
    [data-testid="stSidebar"] a:hover::before {
        width: 300px;
        height: 300px;
    }

    [data-testid="stSidebar"] .nav-link span, 
    [data-testid="stSidebar"] a span {
        position: relative;
        z-index: 1;
        transition: all 0.3s ease;
    }

    [data-testid="stSidebar"] .nav-link:hover span, 
    [data-testid="stSidebar"] a:hover span {
        letter-spacing: 1px;
        color: #ffffff !important; /* Ensure span text is white */
    }

    [data-testid="stSidebar"] .nav-link:hover, 
    [data-testid="stSidebar"] a:hover {
        box-shadow: 0 0 15px rgba(106, 17, 203, 0.5),
                    0 0 25px rgba(37, 117, 252, 0.3) !important;
    }

    [data-testid="stSidebar"] .nav-link:active, 
    [data-testid="stSidebar"] a:active {
        transform: scale(0.98) !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2) !important;
    }

    /* Streamlit-specific class alignment */
    .st-emotion-cache-1y4p8pa {
        padding: 12px 20px !important;
        border-radius: 12px !important;
        margin-bottom: 10px !important;
        background: rgba(255, 255, 255, 0.9) !important;
        border-left: 5px solid transparent !important;
        transition: all 0.3s ease-in-out !important;
        position: relative !important;
        overflow: hidden !important;
        font-weight: 500 !important;
        color: #333 !important;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1) !important;
    }

    .st-emotion-cache-1y4p8pa:hover {
        background: linear-gradient(135deg, #6a11cb 0%, #2575fc 100%) !important;
        color: #ffffff !important; /* White text on hover */
        border-left: 5px solid #fff !important;
        transform: translateX(8px) scale(1.02) !important;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2),
                    0 0 15px rgba(106, 17, 203, 0.5) !important;
    }

    .st-emotion-cache-1y4p8pa::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s ease, height 0.6s ease;
        z-index: 0;
    }

    .st-emotion-cache-1y4p8pa:hover::before {
        width: 300px;
        height: 300px;
    }
    
    .btn-nav {
        background-color: #6a11cb;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 8px 25px;
        font-weight: bold;
        transition: all 0.3s;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    .btn-nav:hover {
        background-color: #2575fc;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        padding: 15px 0;
        background: linear-gradient(135deg, #6a11cb, #2575fc);
        color: white;
        text-align: center;
        font-size: 16px;
        border-radius: 15px 15px 0 0;
        box-shadow: 0px -4px 12px rgba(0, 0, 0, 0.1);
    }
    
    /* Bouncing animation for chat button */
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
        40% {transform: translateY(-15px);}
        60% {transform: translateY(-7px);}
    }
    
    .chatbot-button {
        animation: bounce 5s infinite;
    }
    
    /* Slide Show Enhancements */
    .slideshow-container {
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
    }
    
    .mySlides img {
        border-radius: 15px;
        transition: transform 0.5s;
    }
    
    .mySlides:hover img {
        transform: scale(1.03);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar with animated links
with st.sidebar:
    # Add animated logo
    st.markdown('<div class="floating">', unsafe_allow_html=True)
    st.image("logo - Copy.jpg", width=150)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>🌈 Navigate</h3>", unsafe_allow_html=True)
    
    # Animated menu items
    st.page_link("D:/ALL CODE/home_page.py", label="🏠 Home")
    st.page_link("http://localhost:8502/", label="👨‍👩‍👧‍👦 About Us")
    st.page_link("http://localhost:8503/", label="🏆 Our Motivation")
    st.page_link("http://localhost:8504/", label="🧠 Model")
    st.page_link("http://localhost:8505/", label="📊 Dashboard")
    st.page_link("http://localhost:8506/", label="💬 Chatbot")
    st.page_link("http://localhost:8507/", label="😊 Feedback")
    
    # Fun fact for kids section
    st.markdown("---")
    
    fun_facts = [
        "Did you know? Your brain uses about 20% of all the oxygen you breathe! 🧠",
        "Laughing is like exercise for your brain! It releases happy chemicals. 😂",
        "Your brain has about 100 billion neurons. That's more than stars in our galaxy! ✨",
        "Getting enough sleep helps your brain learn new things better! 😴",
        "Exercise not only makes your body stronger but your brain too! 🏃‍♀️"
    ]
    
    if "fun_fact_index" not in st.session_state:
        st.session_state.fun_fact_index = 0
    
    st.markdown(
        f"""
        <div style='background: rgba(255, 255, 255, 0.8); padding: 15px; border-radius: 10px; margin-top: 20px;'>
            <h4 style='color: #6a11cb;'>🌟 Fun Fact!</h4>
            <p>{fun_facts[st.session_state.fun_fact_index]}</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Change fun fact every 10 seconds
    if "last_fact_time" not in st.session_state:
        st.session_state.last_fact_time = time.time()
        
    if time.time() - st.session_state.last_fact_time >= 10:
        st.session_state.fun_fact_index = (st.session_state.fun_fact_index + 1) % len(fun_facts)
        st.session_state.last_fact_time = time.time()

# Main content with floating animation
with st.container():
    # Animated heading with rainbow effect and black border
    st.markdown("<h1 class='rainbow-text'>Child Mental Health</h1>", unsafe_allow_html=True)
    
    # Updated intro text with new styling
    st.markdown("""
        <p class='intro-text'>
            Helping children understand and manage their thoughts and feelings for a happier, healthier life! 
            Our website is specially designed for children aged 5-15 and their parents.
        </p>
    """, unsafe_allow_html=True)

# Enhanced quotes section with animations
st.markdown("<h2 style='margin-top: 25px;'>✨ Inspiring Thoughts</h2>", unsafe_allow_html=True)

import streamlit as st
import streamlit.components.v1 as components
import json

# Quotes data
quotes = [
    {
        "text": "Children's mental health is just as important as their physical health and deserves the same quality of support.",
        "author": "Kate Middleton",
        "icon": "🌞",
        "color": "linear-gradient(135deg, #FF5733, #FF8C42)"
    },
    {
        "text": "The greatest gifts you can give your children are the roots of responsibility and the wings of independence.",
        "author": "Denis Waitley",
        "icon": "💖",
        "color": "linear-gradient(135deg, #28A745, #5FD068)"
    },
    {
        "text": "A child's mental health is the foundation of their future happiness and success.",
        "author": "Jack Shonkoff",
        "icon": "🌈",
        "color": "linear-gradient(135deg, #007BFF, #00C6FF)"
    },
    {
        "text": "Every child you encounter is a divine appointment.",
        "author": "Wess Stafford",
        "icon": "✨",
        "color": "linear-gradient(135deg, #8E44AD, #AC66CC)"
    }
]

# Convert quotes to a proper JSON string
quotes_js = json.dumps(quotes)

# HTML and JavaScript for auto-switching quotes
components.html(
    f"""
    <div id="quote-container" class="quote-container" style="background: linear-gradient(135deg, #6a11cb, #2575fc); border-radius: 10px; padding: 20px; margin: 15px 0; box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);"></div>
    <div style="display: flex; justify-content: center; gap: 20px; margin-top: 10px;">
        <button id="prev-quote-btn" style="background-color: #6a11cb; color: white; border: none; border-radius: 25px; padding: 8px 25px; font-weight: bold; transition: all 0.3s; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); cursor: pointer;">❮ Previous</button>
        <button id="next-quote-btn" style="background-color: #6a11cb; color: white; border: none; border-radius: 25px; padding: 8px 25px; font-weight: bold; transition: all 0.3s; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); cursor: pointer;">Next ❯</button>
    </div>
    <script>
        (function() {{
            console.log("Quotes JavaScript loaded");
            let quotes = {quotes_js};
            console.log("Parsed quotes:", quotes);

            let quoteIndex = 0;

            function displayQuote(index) {{
                const container = document.getElementById('quote-container');
                if (!container) {{
                    console.error("Quote container not found");
                    return;
                }}

                if (index < 0 || index >= quotes.length) {{
                    console.error("Invalid quote index:", index);
                    return;
                }}

                const quote = quotes[index];
                console.log("Displaying quote:", quote.text);
                
                container.style.background = quote.color;
                container.innerHTML = `
                    <h3 style="color: white; font-size: 28px; margin-bottom: 15px;">${{quote.icon}} Thought of the Day</h3>
                    <p style="color: white; font-size: 22px; font-weight: 500; font-style: italic;">"${{quote.text}}"</p>
                    <p style="font-size: 16px; color: rgba(255, 255, 255, 0.9); text-align: right;">— ${{quote.author}}</p>
                `;
            }}

            function nextQuote() {{
                quoteIndex = (quoteIndex + 1) % quotes.length;
                console.log("Switching to next quote, index:", quoteIndex);
                displayQuote(quoteIndex);
            }}

            function prevQuote() {{
                quoteIndex = (quoteIndex - 1 + quotes.length) % quotes.length;
                console.log("Switching to previous quote, index:", quoteIndex);
                displayQuote(quoteIndex);
            }}

            // Attach event listeners to buttons
            const nextButton = document.getElementById('next-quote-btn');
            const prevButton = document.getElementById('prev-quote-btn');

            if (nextButton) {{
                nextButton.addEventListener('click', nextQuote);
                console.log("Next button event listener attached");
            }}

            if (prevButton) {{
                prevButton.addEventListener('click', prevQuote);
                console.log("Previous button event listener attached");
            }}

            // Initial display
            displayQuote(quoteIndex);

            // Auto-switch every 8 seconds
            setInterval(nextQuote, 5000);
        }})();
    </script>
    """,
    height=300
)

# Enhanced slideshow with better transitions and animations
components.html(
    """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {box-sizing: border-box;}
body {font-family: 'Poppins', sans-serif; background: transparent;}
.mySlides {display: none;}
img {vertical-align: middle;}

/* Slideshow container */
.slideshow-container {
  max-width: 1000px;
  position: relative;
  margin: 0 auto;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

/* Caption text */
.text {
  color: #fff;
  font-size: 18px;
  padding: 15px 20px;
  position: absolute;
  bottom: 0;
  width: 100%;
  text-align: center;
  background: linear-gradient(0deg, rgba(0,0,0,0.7) 0%, rgba(0,0,0,0) 100%);
  border-radius: 0 0 20px 20px;
}

/* Number text (1/4 etc) */
.numbertext {
  color: #fff;
  font-size: 14px;
  padding: 10px 15px;
  position: absolute;
  top: 0;
  background: rgba(0,0,0,0.3);
  border-radius: 0 0 10px 0;
}

/* The dots/bullets/indicators */
.dot-container {
  text-align: center;
  padding: 15px 0;
}

.dot {
  height: 12px;
  width: 12px;
  margin: 0 5px;
  background-color: #bbb;
  border-radius: 50%;
  display: inline-block;
  transition: background-color 0.6s ease;
  cursor: pointer;
}

.active {
  background-color: #6a11cb;
  transform: scale(1.2);
}

/* Fading animation */
.fade {
  animation-name: fade;
  animation-duration: 1.5s;
}

@keyframes fade {
  from {opacity: 0.4} 
  to {opacity: 1}
}

/* Image hover effect */
.mySlides img {
  transition: transform 0.5s;
  width: 100%;
  height: 70vh;
  object-fit: cover;
}

.mySlides:hover img {
  transform: scale(1.03);
}

/* Add image captions */
.caption {
  position: absolute;
  bottom: 20px;
  width: 100%;
  background: rgba(0,0,0,0.6);
  color: white;
  padding: 15px;
  font-size: 18px;
  text-align: center;
}

/* Image overlay on hover */
.overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(106, 17, 203, 0.2);
  opacity: 0;
  transition: opacity 0.5s;
}

.mySlides:hover .overlay {
  opacity: 1;
}
</style>
</head>
<body>

<div class="slideshow-container">

<div class="mySlides fade">
  <div class="numbertext">1 / 4</div>
  <img src="https://www.mpowerminds.com/assetOLD/images/psychiatrist_in_mumbaisd.jpg">
  <div class="overlay"></div>
  <div class="caption">Understanding children's mental health needs</div>
</div>

<div class="mySlides fade">
  <div class="numbertext">2 / 4</div>
  <img src="https://domf5oio6qrcr.cloudfront.net/medialibrary/14528/3f85b1b1-9dc7-4a90-855c-dc204646e889.jpg">
  <div class="overlay"></div>
  <div class="caption">Building emotional strength together</div>
</div>

<div class="mySlides fade">
  <div class="numbertext">3 / 4</div>
  <img src="https://eskimo3.ie/wp-content/uploads/2023/02/36.-mental-health.jpg">
  <div class="overlay"></div>
  <div class="caption">Creating a supportive environment</div>
</div>

<div class="mySlides fade">
  <div class="numbertext">4 / 4</div>
  <img src="https://kickstarterz.co.uk/wp-content/uploads/2021/02/children-and-mental-health.png">
  <div class="overlay"></div>
  <div class="caption">Growing happier, healthier children</div>
</div>

</div>
<br>

<div class="dot-container">
  <span class="dot" onclick="currentSlide(1)"></span> 
  <span class="dot" onclick="currentSlide(2)"></span> 
  <span class="dot" onclick="currentSlide(3)"></span>
  <span class="dot" onclick="currentSlide(4)"></span>
</div>

<script>
let slideIndex = 0;
let timeoutId;
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
  timeoutId = setTimeout(showSlides, 5000); // Change image every 5 seconds
}

function currentSlide(n) {
  clearTimeout(timeoutId);
  slideIndex = n - 1;
  showSlides();
}
</script>

</body>
</html> 
    """,
    height=700
)

# Enhanced activities for kids section
st.markdown("<h2 style='margin-top: 30px;'>🎮 Fun Activities for Kids</h2>", unsafe_allow_html=True)

# Display 3 activity cards in columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="background: white; padding: 20px; border-radius: 15px; height: 100%; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: transform 0.3s;">
        <h3 style="color: #28A745;">🧩 Social Media & Emotional Wellbeing</h3>
        <p>Let's explore how social media affects your emotions. Join the Game..</p>
        <a href="http://localhost:8508/" class="btn-nav" style="display: inline-block; padding: 10px 20px; background-color: #2846a7; color: white; text-decoration: none; border-radius: 5px; text-align: center;">Play</a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 20px; border-radius: 15px; height: 100%; box-shadow: 0 4px 10px rgba(0,0,0,0.1); transition: transform 0.3s;">
        <h3 style="color: #28A745;">😊 Social Media Emotion Explorer</h3>
        <p>Match emotions with faces and situations in our fun interactive puzzle game!</p>
        <a href="http://localhost:8509/" class="btn-nav" style="display: inline-block; padding: 10px 20px; background-color: #2846a7; color: white; text-decoration: none; border-radius: 5px; text-align: center;">Play</a>
    </div>
    """, unsafe_allow_html=True)


import streamlit as st
import streamlit.components.v1 as components

# Define the HTML for the chatbot button with improved visibility
chatbot_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            /* Chatbot button container */
            .chat-button-container {
                position: fixed;
                bottom: 34px;
                right: 20px;
                z-index: 9999;
                width: 60px;
                height: 60px;
            }
            
            /* Chatbot button */
            .chat-button {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #0056b3, #007bff);
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
                cursor: pointer;
                border: 2px solid #fff;
                transition: all 0.3s ease;
                text-decoration: none;
            }
            
            .chat-button:hover {
                transform: scale(1.05);
                box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
                background: linear-gradient(135deg, #004494, #0062cc);
            }
            
            /* Chat icon */
            .chat-icon {
                font-size: 28px;
                color: white;
                text-align: center;
            }
            
            /* Pulse animation */
            @keyframes pulse {
                0% { box-shadow: 0 0 0 0 rgba(0, 123, 255, 0.7); }
                70% { box-shadow: 0 0 0 10px rgba(0, 123, 255, 0); }
                100% { box-shadow: 0 0 0 0 rgba(0, 123, 255, 0); }
            }
            
            .chat-button {
                animation: pulse 2s infinite;
            }
        </style>
    </head>
    <body>
        <div class="chat-button-container">
            <a href="http://localhost:8506/" class="chat-button" target="_blank">
                <span class="chat-icon">💬</span>
            </a>
        </div>
    </body>
    </html>
"""

# Add this near the end of your Streamlit app, just before the footer
# Make sure to use a sufficient height to ensure visibility
components.html(chatbot_html, height=120, width=100)

# Parent resources section
st.markdown("<h2 style='margin-top: 30px;'>👨‍👩‍👧‍👦 For Parents</h2>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); height: 100%;">
        <h3 style="color: #6a11cb;">📚 Latest Resources</h3>
        <ul style="padding-left: 20px;">
            <li>How to talk to your child about anxiety</li>
            <li>Building resilience in children aged 5-10</li>
            <li>Screen time: Finding the right balance</li>
            <li>Supporting your teen's emotional health</li>
        </ul>
        <button class="btn-nav" style="margin-top: 15px;">Read More</button>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); height: 100%;">
        <h3 style="color: #6a11cb;">🗓️ Upcoming Webinars</h3>
        <p><strong>April 5:</strong> Understanding childhood anxiety</p>
        <p><strong>April 12:</strong> Helping children process difficult emotions</p>
        <p><strong>April 20:</strong> Building healthy digital habits</p>
        <button class="btn-nav" style="margin-top: 15px;">Register Now</button>
    </div>
    """, unsafe_allow_html=True)

# Enhanced footer
st.markdown(
    """
    <div class="footer">
        <div style="display: flex; justify-content: space-around; align-items: center; padding: 0 20px;">
            <span>© Copyright 2025 Child Mental Health, India</span>
            <div>
                <span style="margin: 0 10px;">📞 Helpline: 1800-123-4567</span>
                <span style="margin: 0 10px;">📧 support@childmentalhealth.org</span>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# JavaScript to ensure animations apply correctly
components.html(
    """
    <script>
    document.addEventListener('DOMContentLoaded', function() {
        // Force reapplication of styles for sidebar links
        const sidebarLinks = document.querySelectorAll('[data-testid="stSidebar"] a');
        sidebarLinks.forEach(link => {
            link.style.transition = 'all 0.3s ease-in-out';
            link.addEventListener('mouseover', function() {
                this.style.transform = 'translateX(8px) scale(1.02)';
                this.style.color = '#ffffff'; // Force white text on hover
                this.style.webkitTextFillColor = '#ffffff'; // Ensure compatibility
                this.style.textShadow = '0 1px 2px rgba(0, 0, 0, 0.3)'; // Add shadow for contrast
            });
            link.addEventListener('mouseout', function() {
                this.style.transform = 'translateX(0) scale(1)';
                this.style.color = '#333'; // Reset to default color
                this.style.webkitTextFillColor = '#333';
                this.style.textShadow = 'none'; // Remove shadow
            });
        });

        // Gentle floating animation for other elements
        const floatingElements = document.querySelectorAll('.quote-container, .btn-nav');
        floatingElements.forEach(elem => {
            elem.addEventListener('mouseover', function() {
                this.style.transform = 'translateY(-5px)';
                this.style.boxShadow = '0 10px 20px rgba(0,0,0,0.2)';
            });
            elem.addEventListener('mouseout', function() {
                this.style.transform = 'translateY(0)';
                this.style.boxShadow = '0 4px 10px rgba(0,0,0,0.1)';
            });
        });
    });
    </script>
    """,
    height=0
)

# Add balloon animation when page loads (fun for kids)
if "has_shown_balloons" not in st.session_state:
    st.session_state.has_shown_balloons = True
    st.balloons()
