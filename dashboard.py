import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components

# Set page configuration
st.set_page_config(
    page_title="Child Mental Health Dashboard",
    page_icon="📊",
    layout="wide",
)

# Sidebar Navigation
with st.sidebar:
    selected = option_menu(
        "Dashboard Menu",
        ["Overview", "Social Media Usage", "Mental Health Insights", "Recommendations"],
        icons=["house", "phone", "heart", "list-task"],
        menu_icon="cast",
        default_index=0,
    )

# Title and Header
st.markdown(
    """<style>.main {background-color: #f0f2f6;}</style>""",
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div style="background-color:#6c63ff;padding:10px;border-radius:10px">
    <h1 style="color:white;text-align:center;">Child Mental Health Dashboard</h1>
    <h3 style="color:white;text-align:center;">Empowering Parents to Monitor and Support Their Children</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

# Sample Data (Replace this with real data later)
data = {
    "Age Group": ["5-7", "8-10", "11-12", "12-13", "15"],
    "Screen Time (hrs)": [1.5, 2.5, 3.0, 4.0, 5.0],
    "Mood Rating (1-10)": [8, 7, 6, 5, 4],
}
df = pd.DataFrame(data)

# Conditional Display Based on Menu Selection
if selected == "Overview":
    st.subheader("Overview")
    st.write("Welcome to the Child Mental Health Dashboard. Navigate through the menu to access insights and recommendations tailored to support your child.")

    components.iframe("https://app.powerbi.com/reportEmbed?reportId=f83310e4-1d35-4b7c-a7b9-468eac44989f&autoAuth=true&ctid=cca3f0fe-586f-4426-a8bd-b8146307e738", height=500)

elif selected == "Social Media Usage":
    st.subheader("Social Media Usage")
    fig = px.bar(df, x="Age Group", y="Screen Time (hrs)", title="Average Screen Time by Age Group", color="Age Group")
    st.plotly_chart(fig, use_container_width=True)

    avg_screen_time = df["Screen Time (hrs)"].mean()
    st.info(f"Average Screen Time Across Age Groups: {avg_screen_time:.2f} hours")

elif selected == "Mental Health Insights":
    st.subheader("Mental Health Insights")
    fig = px.scatter(df, x="Screen Time (hrs)", y="Mood Rating (1-10)",
                     title="Screen Time vs. Mood Rating",
                     color="Mood Rating (1-10)", size="Screen Time (hrs)",
                     labels={"Mood Rating (1-10)": "Mood Rating"})
    st.plotly_chart(fig, use_container_width=True)

    st.write("Analyzing correlations between screen time and mood ratings helps identify trends that may impact mental health.")

elif selected == "Recommendations":
    st.subheader("Recommendations")
    st.write("Here are some personalized recommendations based on the observed data:")
    st.markdown("""
    - Set screen time limits for children and encourage offline activities.
    - Promote physical activities like sports or outdoor games.
    - Monitor the type of content consumed on social media.
    - Have regular conversations about their emotions and well-being.
    """)

# Footer
st.markdown(
    """
    <hr style="border:1px solid #6c63ff;">
    <p style="text-align:center;color:gray;">&copy; 2025 Child Mental Health Dashboard | Final Year Engineering Project</p>
    """,
    unsafe_allow_html=True,
)
