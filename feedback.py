import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime

# Google Sheets API setup
SHEET_NAME = "Feedback"  # Change to your Google Sheet name

# Authenticate and connect to Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open(SHEET_NAME).sheet1  

st.header("Your Feedback Matters a lot for us..")

# User feedback form
model_output = st.selectbox("Are you satisfied with the model output?", ['','Strongly Agree', 'Agree', 'Disagree'], key='model_output')


dashboard = st.selectbox("To what extent do you feel the insights provided by the dashboard were helpful?", ['','Strongly Agree', 'Agree', 'Disagree'], key='dashboard')
chatbot = st.selectbox("Did the chatbot solve your queries?", ['','Strongly Agree', 'Agree', 'Disagree'], key='chatbot')
experience = st.selectbox("How was your overall experience with the website?", ['','Outstanding', 'Very Good', 'Fair'], key='experience')
improvements = st.text_area("Do you feel any need for improvements on the website?", key='improvements')

# Submit button
if st.button("Submit"):
    try:
        # Store the data in Google Sheets
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, model_output, dashboard, chatbot, experience, improvements])

        st.success("✅ Thank you for your feedback! Your response has been recorded.")
    except Exception as e:
        st.error(f"❌ Error saving data: {e}")
