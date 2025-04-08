import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import pathlib

# Configure page settings
st.set_page_config(page_title="Feedback Page..", layout="wide", page_icon="😇")

# Function to load CSS from the 'assets' folder
def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# Load the external CSS
css_path = pathlib.Path("assets/styles.css")
load_css(css_path)


# Google Sheets API setup
SHEET_NAME = "Feedback"  # Change to your Google Sheet name

# Authenticate and connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open(SHEET_NAME).sheet1  

st.header("Your Feedback Matters a lot for us..  	    :innocent:")

st.write("")
st.write("")
# User feedback form
model_output = st.selectbox("Are you satisfied with the model output?", ['','Strongly Agree', 'Agree', 'Disagree'], key='model_output')


dashboard = st.selectbox("To what extent do you feel the insights provided by the dashboard were helpful?", ['','Strongly Agree', 'Agree', 'Disagree'], key='dashboard')
chatbot = st.selectbox("Did the chatbot solve your queries?", ['','Strongly Agree', 'Agree', 'Disagree'], key='chatbot')
experience = st.selectbox("How was your overall experience with the website?", ['','Outstanding', 'Very Good', 'Fair'], key='experience')
improvements = st.text_area("Do you feel any need for improvements on the website?", key='improvements')


st.write("#")

# Submit button
if st.button("Submit", key="green"):
    try:
        # Store the data in Google Sheets
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, model_output, dashboard, chatbot, experience, improvements])

        st.success("✅ Thank you for your feedback! Your response has been recorded.")
    except Exception as e:
        st.error(f"❌ Error saving data: {e}")
