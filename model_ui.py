import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
import seaborn as sns

# Load trained model and scaler
rf_model = joblib.load("RANDOM_FOREST_MODEL.pkl")
scaler = joblib.load("SCALER.pkl")
trained_features = joblib.load("TRAINED_FEATURES.pkl")

# Define categorical options for user selection
categorical_options = {
    'SCHOOL_SECTION': ['Primary_section', 'Secondary_section', 'Higher_secondary_section'],
    'PERSONAL_SMARTPHONE': ['Yes', 'No'],
    'TELEVISION_SCREEN_TIME': ['Less than 1 hour', '1 to 3 hours', '3 to 5 hours', 'More than 5 hours'],
    'PHONE_SCREEN_TIME': ['Less than 1 hour', 'Between 1 hour & 3 hours', 'Between 3 hours & 5 hours', 'More than 5 hours'],
    'SOCIAL_MEDIA_PLATFORM': [],  # Multi-select
    'SOCIAL_MEDIA_CONTENT': [],  # Multi-select
    'MOBILE_GAMES': [],  # Multi-select
    'SLEEPING_TIME': ['Before 10pm', 'Between 10pm and 12am', 'After midnight 12am'],
    'WAKEUP_TIME': ['By 8am', 'Between 8am to 10am', 'After 10am'],
    'OUTDOOR_SPORTS': ['Low', 'Moderate', 'High'],
    'SLEEP_ISSUES': ['Low', 'Moderate', 'High'],
    'DISTRACTION_DURING_SLEEPING': ['Low', 'Moderate', 'High'],
    'EYES_STRAINED': ['Yes', 'No'],
    'SPECTACLES': ['Yes', 'No'],
    'SPECTACLE_NUMBER': ['Between 1 and 3', 'Between 3 and 5', 'Less than 1', 'More than 5', 'No spectacle'],
    'RESTLESS': ['Low', 'Moderate', 'High'],
    'DISTRACTION_DURING_SEARCHING': ['Low', 'Moderate', 'High'],
    'LACK_OF_CONCENTRATION': ['Low', 'Moderate', 'High'],
    'ANXIETY': ['Low', 'Moderate', 'High'],
    'BEHAVIOURAL_CHANGES': ['Low', 'Moderate', 'High'],
    'REPLICATE_SOCIAL_MEDIA': ['Low', 'Moderate', 'High']
}

# Streamlit UI
st.title("Depression Level Prediction")
st.write("#")

# User Inputs
age = st.slider("Age (5 to 15 years)", 5, 15, 10)
gender = st.radio("Gender", ["Male", "Female"])
ott_subscription = st.radio("OTT Subscription", ["Yes", "No"])

# Multi-select categorical inputs
television_content_options = ['Cartoon', 'Movies', 'Sports', 'News', 'Others']
selected_tv_content = st.multiselect("Select Television Content Type", television_content_options)
categorical_options['TELEVISION_CONTENT'] = selected_tv_content

social_media_platform_options = ['Youtube', 'Instagram', 'Snapchat', 'Facebook', 'Tiktok', 'Others']
selected_social_media_platform = st.multiselect("Select Social Media Platforms Used", social_media_platform_options)
categorical_options['SOCIAL_MEDIA_PLATFORM'] = selected_social_media_platform

social_media_content_options = ['Entertainment', 'Educational', 'Negative', 'Casual_scrolling']
selected_social_media_content = st.multiselect("Select Social Media Content Type", social_media_content_options)
categorical_options['SOCIAL_MEDIA_CONTENT'] = selected_social_media_content

mobile_games_options = ['Action', 'Racing', 'Puzzles', 'Others']
selected_mobile_games = st.multiselect("Select Mobile Game Types Played", mobile_games_options)
categorical_options['MOBILE_GAMES'] = selected_mobile_games

# Collect categorical inputs
categorical_values = {}
for feature, options in categorical_options.items():
    if feature not in ['TELEVISION_CONTENT', 'SOCIAL_MEDIA_PLATFORM', 'SOCIAL_MEDIA_CONTENT', 'MOBILE_GAMES']:
        categorical_values[feature] = st.selectbox(feature.replace("_", " "), options)
    else:
        categorical_values[feature] = options

# Convert lists to strings for multi-select inputs
for key, value in categorical_values.items():
    if isinstance(value, list):
        categorical_values[key] = ", ".join(value)

# Convert user input into a DataFrame
input_data = pd.DataFrame([categorical_values])

# Apply pd.get_dummies to categorical data
input_data = pd.get_dummies(input_data)

# Convert categorical inputs to numerical
gender = 1 if gender == "Male" else 0
ott_subscription = 1 if ott_subscription == "Yes" else 0

# Ensure input data matches trained feature set
missing_cols = set(trained_features) - set(input_data.columns)
missing_data = pd.DataFrame(0, index=input_data.index, columns=list(missing_cols))
input_data = pd.concat([input_data, missing_data], axis=1)
input_data = input_data[trained_features]

# Insert numerical fields
if "AGE" not in input_data.columns:
    input_data.insert(0, "AGE", age)
else:
    input_data["AGE"] = age

if "GENDER" not in input_data.columns:
    input_data.insert(1, "GENDER", gender)
else:
    input_data["GENDER"] = gender

if "OTT_SUBSCRIPTION" not in input_data.columns:
    input_data.insert(2, "OTT_SUBSCRIPTION", ott_subscription)
else:
    input_data["OTT_SUBSCRIPTION"] = ott_subscription

# Convert screen time input into numerical values for visualization
screen_time_mapping = {
    'Less than 1 hour': 0.5,
    'Between 1 hour & 3 hours': 2,
    'Between 3 hours & 5 hours': 4,
    'More than 5 hours': 6
}
child_screen_time = screen_time_mapping[categorical_values['PHONE_SCREEN_TIME']]

# Recommended screen time based on age groups
if 5 < age <= 8:
    recommended_screen_time = 1  # Less than 1 hour recommended
elif 9 < age <= 12:
    recommended_screen_time = 2  # 1-2 hours recommended
elif 13 < age <= 15:
    recommended_screen_time = 3  # Max 2-3 hours recommended

st.write("#")

# Depression Level Tips (without emojis)
def get_tips(depression_level):
    if depression_level == "Low":
        return """
        Resources for Well-Being:
        Apps: Moodpath, Woebot, Headspace, Calm (for mindfulness and mood tracking).  
        Books: Feeling Good by Dr. David Burns, The Happiness Trap by Dr. Russ Harris.  
        Online Tools: Mental Health America (MHA) screening tools, Mind.org.uk resources.  

        Tips for Maintaining Good Mental Health:
        - Self-Care: Prioritize sleep, nutrition, and hydration. Establish a daily routine.  
        - Exercise: Engage in light physical activity like walking, yoga, or stretching (30 minutes/day).  
        - Mindfulness: Practice meditation, deep breathing, or journaling to manage stress.  
        - Social Connection: Stay connected with friends or family, even if it’s just a quick chat.  
        - Hobbies: Engage in activities you enjoy, like reading, art, or gardening.  
        """
    elif depression_level == "Moderate":
        return """
        Resources for Coping:
        Apps: Sanvello, Happify, BetterHelp (for stress management and therapy).  
        Books: The Mindful Way Through Depression by Mark Williams, Atomic Habits by James Clear.  
        Online Tools: Verywell Mind - Coping Strategies.  

        Coping Strategies:
        - Structured Routine: Stick to a daily plan to bring stability.  
        - Physical Health: Engage in moderate exercise, eat healthy, and hydrate.  
        - Emotional Check-ins: Keep a journal and reflect on emotions.  
        - Limit Social Media: Reduce negative online exposure and focus on uplifting content.  
        """
    elif depression_level == "High":
        return """
        Seeking Professional Help:
        Apps: Talkspace, BetterHelp, 7 Cups (for online therapy and emotional support).  
        Books: Lost Connections by Johann Hari, The Depression Cure by Stephen Ilardi.  
        Helplines: Find a Therapist - Psychology Today, NIMH - Find Help.  

        What You Can Do:
        - Reach Out: Talk to a trusted friend, family member, or counselor.  
        - Seek Therapy: Professional help can guide you towards recovery.  
        - Medical Advice: Consult a doctor if symptoms persist or worsen.  
        - Crisis Support: If you have severe distress, seek emergency help or a hotline service.  
        """

# Function to generate PDF
def generate_pdf(depression_level, tips_content, recommended_screen_time, child_screen_time, graph_image, user_inputs):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Add content to PDF
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, height - 50, "Depression Level Prediction Report")
    c.setFont("Helvetica", 12)

    # Add user inputs section
    c.drawString(30, height - 80, "User Inputs:")
    y_position = height - 100
    for key, value in user_inputs.items():
        c.drawString(30, y_position, f"{key.replace('_', ' ')}: {value}")
        y_position -= 20
        if y_position < 100:  # Prevent text from going off the page
            c.showPage()
            y_position = height - 50

    # Add predicted depression level
    c.drawString(30, y_position - 20, f"Predicted Depression Level: {depression_level}")
    y_position -= 40

    # Add tips and recommendations
    c.drawString(30, y_position, "Tips and Recommendations:")
    text = c.beginText(30, y_position - 20)
    text.setFont("Helvetica", 10)
    for line in tips_content.split("\n"):
        text.textLine(line.strip())
    c.drawText(text)
    y_position -= 120

    # Add screen time comparison
    c.drawString(30, y_position, "Screen Time Comparison:")
    c.drawString(30, y_position - 20, f"Recommended Screen Time: {recommended_screen_time} hours/day")
    c.drawString(30, y_position - 40, f"Your Screen Time: {child_screen_time} hours/day")
    y_position -= 80

    # Add graph image to PDF
    c.drawString(30, y_position, "Screen Time Visualization:")
    c.drawImage(ImageReader(graph_image), 30, y_position - 220, width=400, height=200)

    # Save the PDF
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer

# Prediction button
if st.button("Predict Depression Level"):
    input_scaled = scaler.transform(input_data)
    prediction = rf_model.predict(input_scaled)
    
    depression_level = prediction[0]
    st.subheader(f"Predicted Depression Level: **{depression_level}**")
    
    # Display appropriate tips and resources
    tips_content = get_tips(depression_level)
    st.markdown(tips_content, unsafe_allow_html=True)

    # Visualization: Screen Time Comparison
    st.subheader("📊 Recommended vs. Actual Screen Time")

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=["Recommended", "Your Input"], y=[recommended_screen_time, child_screen_time], palette=["green", "red"], ax=ax)
    ax.set_ylabel("Hours Per Day")
    ax.set_title("Comparison of Recommended vs. Actual Screen Time")
    st.pyplot(fig)

    # Save the graph as an image
    graph_image = BytesIO()
    plt.savefig(graph_image, format='png', bbox_inches='tight')
    plt.close()
    graph_image.seek(0)

    # Display Recommendations
    if depression_level == "High":
        st.warning("🚨 High depression level detected. Consider reducing screen time and seeking professional help.")
    elif depression_level == "Moderate":
        st.info("⚠️ Moderate depression level. Try balancing screen time and engaging in outdoor activities.")
    else:
        st.success("✅ Low depression level. Keep maintaining a healthy balance of screen time.")

    # Prepare user inputs for PDF
    user_inputs = {
        "Age": age,
        "Gender": "Male" if gender == 1 else "Female",
        "OTT Subscription": "Yes" if ott_subscription == 1 else "No",
        **categorical_values
    }

    # Generate PDF
    pdf_buffer = generate_pdf(depression_level, tips_content, recommended_screen_time, child_screen_time, graph_image, user_inputs)
    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer,
        file_name="depression_level_report.pdf",
        mime="application/pdf"
    )
