import streamlit as st
from streamlit_option_menu import option_menu

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
    st.title("Child Mental Health ..")
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()


    st.components.v1.html(html_content, height=300, scrolling=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.html("""
  <style>
    [alt=Logo] {
      height: 8rem;
      width: 8rem;
      border-radius: 20%;
      object-fit: fill;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
      border: 2px solid #007BFF;
    }
  </style>
""")

# Sidebar Navigation
with st.sidebar:
    st.page_link("streamlit_app.py", label="Home", icon=":material/home:")
    st.page_link("http://localhost:8504/", label="Dashboard", icon=":material/dashboard:")
    st.page_link("http://localhost:8504/", label="Model", icon=":material/model_training:")
    st.page_link("http://localhost:8504/", label="Chatbot", icon=":material/forum:")
    st.page_link("http://localhost:8504/", label="About Us", icon=":material/groups:")
