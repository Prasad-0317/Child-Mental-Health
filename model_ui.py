import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup

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
    'SOCIAL_MEDIA_PLATFORM': [],
    'SOCIAL_MEDIA_CONTENT': [],
    'MOBILE_GAMES': [],
    'SLEEPING_TIME': ['Before 10pm', 'Between 10pm and 12am', 'After midnight 12am'],
    'WAKEUP_TIME': ['By 8am', 'Between 8am to 10am', 'After 10am'],
    'What type of food does the child mostly consume?': ['Healthy (Home-cooked meals, fruits, vegetables, balanced diet)', 'Unhealthy (Fast food, sugary snacks, processed foods)', 'Mixed (A balance of both healthy and unhealthy food)'],
    'What type of books does the child mostly read?': ['Storybooks (Fairy tales, adventure, fiction)', 'Educational/Inspirational (Academic, biographies, self-improvement)', 'Comics & Graphic Novels', 'Fantasy & Science Fiction'],
    'How often does the child experience conflicts or arguments at home?': ['Rarely (Almost never)', 'Occasionally (Once in a while)', 'Frequently (Several times a week)', 'Very Often (Almost every day)'],
    'Does the child feel comfortable sharing their thoughts and emotions at home?': ['Yes, always', 'Sometimes', 'Rarely', 'No, never'],
    'How much quality time does the family spend together?': ['A lot (Daily bonding activities, meals together, outings, etc.)', 'Moderate (Some shared activities but not every day)', 'Limited (Occasional interactions but mostly independent)', 'Very little (Rarely spend time together)'],
    'How would you describe the overall environment at home ?': ['Mostly Positive (Occasional disagreements but generally supportive)', 'Neutral (Neither too positive nor negative)', 'Mostly Negative (Frequent arguments or stress)'],
    'HOBBIES': [],
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
categorical_options['TELEVISION_CONTENT'] = [', '.join(selected_tv_content)]

social_media_platform_options = ['Youtube', 'Instagram', 'Snapchat', 'Facebook', 'Tiktok', 'Others']
selected_social_media_platform = st.multiselect("Select Social Media Platforms Used", social_media_platform_options)
categorical_options['SOCIAL_MEDIA_PLATFORM'] = [', '.join(selected_social_media_platform)]

social_media_content_options = ['Entertainment', 'Educational', 'Negative', 'Casual_scrolling']
selected_social_media_content = st.multiselect("Select Social Media Content Type", social_media_content_options)
categorical_options['SOCIAL_MEDIA_CONTENT'] = [', '.join(selected_social_media_content)]

mobile_games_options = ['Action', 'Racing', 'Puzzles', 'Others']
selected_mobile_games = st.multiselect("Select Mobile Game Types Played", mobile_games_options)
categorical_options['MOBILE_GAMES'] = [', '.join(selected_mobile_games)]

hobbies_options = ['Drawing & Painting', 'Playing musical instruments', 'Dancing', 'Outdoor activities(like swimming, badminton, etc.)']
selected_hobbies = st.multiselect("What are the child's hobbies?", hobbies_options)
categorical_options['HOBBIES'] = [', '.join(selected_hobbies)]

# Collect categorical inputs
categorical_values = {}
for feature, options in categorical_options.items():
    if feature not in ['TELEVISION_CONTENT', 'SOCIAL_MEDIA_PLATFORM', 'SOCIAL_MEDIA_CONTENT', 'MOBILE_GAMES', 'HOBBIES']:
        categorical_values[feature] = st.selectbox(feature.replace("_", " "), options)
    else:
        categorical_values[feature] = options[0] if options else ""

# Convert user input into a DataFrame
input_data = pd.DataFrame([categorical_values])
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

# Convert screen time input into numerical values
screen_time_mapping = {
    'Less than 1 hour': 0.5,
    'Between 1 hour & 3 hours': 2,
    'Between 3 hours & 5 hours': 4,
    'More than 5 hours': 6
}

tele_screen_time_mapping = {
    'Less than 1 hour': 0.5,
    '1 to 3 hours': 2,
    '3 to 5 hours': 4,
    'More than 5 hours': 6
}

food = {
    'Healthy (Home-cooked meals, fruits, vegetables, balanced diet)': 'Healthy',
    'Unhealthy (Fast food, sugary snacks, processed foods)': 'Unhealthy',
    'Mixed (A balance of both healthy and unhealthy food)': 'Mixed'
}

child_screen_time = screen_time_mapping[categorical_values['PHONE_SCREEN_TIME']]
child_tele_screen_time = tele_screen_time_mapping[categorical_values['TELEVISION_SCREEN_TIME']]
child_food = food[categorical_values['What type of food does the child mostly consume?']]

# Recommended screen time based on age groups
if 5 <= age <= 8:
    recommended_screen_time = 1
elif 9 <= age <= 12:
    recommended_screen_time = 3
elif 13 <= age <= 15:
    recommended_screen_time = 4

if 5 <= age <= 8:
    recommended_tele_screen_time = 3.5
elif 9 <= age <= 12:
    recommended_tele_screen_time = 2
elif 13 <= age <= 15:
    recommended_tele_screen_time = 1.5

st.write("#")

# Function to generate customized recommendations
def get_custom_recommendations(depression_level, age, input_data, categorical_values, child_screen_time, child_tele_screen_time, recommended_screen_time, recommended_tele_screen_time, child_food):
    resources = {"Apps": [], "Books": [], "Online Tools": []}
    tips = []

    hobbies = categorical_values.get('HOBBIES', '').split(', ') if categorical_values.get('HOBBIES') else []
    social_media_platforms = categorical_values.get('SOCIAL_MEDIA_PLATFORM', '').split(', ') if categorical_values.get('SOCIAL_MEDIA_PLATFORM') else []
    social_media_content = categorical_values.get('SOCIAL_MEDIA_CONTENT', '').split(', ') if categorical_values.get('SOCIAL_MEDIA_CONTENT') else []
    sleep_time = categorical_values.get('SLEEPING_TIME', '')
    wakeup_time = categorical_values.get('WAKEUP_TIME', '')
    food_type = categorical_values.get('What type of food does the child mostly consume?', '')
    book_type = categorical_values.get('What type of books does the child mostly read?', '')
    family_time = categorical_values.get('How much quality time does the family spend together?', '')
    home_environment = categorical_values.get('How would you describe the overall environment at home ?', '')
    anxiety_level = categorical_values.get('ANXIETY', 'Low')

    if 5 <= age <= 8:
        resources["Apps"].append("GoNoodle - Fun movement and mindfulness for young kids")
        resources["Books"].append("The Very Hungry Caterpillar by Eric Carle - A colorful, engaging story")
        resources["Online Tools"].append("PBS Kids - Educational games and videos")
    elif 9 <= age <= 12:
        resources["Apps"].append("Headspace for Kids - Simple meditation for pre-teens")
        resources["Books"].append("Charlotte's Web by E.B. White - A heartwarming tale")
        resources["Online Tools"].append("Khan Academy Kids - Free learning resources")
    elif 13 <= age <= 15:
        resources["Apps"].append("Calm - Relaxation and sleep support for teens")
        resources["Books"].append("The Giver by Lois Lowry - Thought-provoking fiction")
        resources["Online Tools"].append("Teen Line - Online support for teens")

    if depression_level == "High":
        resources["Apps"].append("BetterHelp - Connect with a therapist")
        resources["Online Tools"].append("Crisis Text Line - Text HOME to 741741 for free support")
    elif depression_level == "Moderate":
        resources["Apps"].append("Daylio - Mood tracking to identify patterns")
    else:
        resources["Apps"].append("Smiling Mind - Free mindfulness exercises")

    if hobbies and hobbies != ['']:
        if "Drawing & Painting" in hobbies:
            resources["Books"].append("How to Draw Cool Stuff by Catherine Holmes - Boost creativity")
        if "Playing musical instruments" in hobbies:
            resources["Online Tools"].append("Simply Piano - Learn piano at your pace")
        if "Dancing" in hobbies:
            resources["Apps"].append("Just Dance Now - Fun dance workouts")
        if "Outdoor activities" in hobbies:
            resources["Books"].append("The Outdoor Adventure Handbook - Explore nature")

    if "Educational/Inspirational" in book_type:
        resources["Books"].append("Who Was Albert Einstein? by Jess Brallier - Inspiring biography")
    elif "Comics & Graphic Novels" in book_type:
        resources["Books"].append("Dog Man by Dav Pilkey - Fun and engaging comics")

    if child_screen_time > recommended_screen_time or child_tele_screen_time > recommended_tele_screen_time:
        tips.append(f"⏰ Cut Back on Screens: Wow, you use screens for {child_screen_time} hrs (phone) and {child_tele_screen_time} hrs (TV)! Try less time and more fun with {hobbies[0] if hobbies else 'playing'}!")
    else:
        tips.append(f"👍 Awesome Screen Time: You’re at {child_screen_time} hrs (phone) and {child_tele_screen_time} hrs (TV)—perfect! Keep it fun with {hobbies[0] if hobbies else 'games'}!")

    if sleep_time == "After midnight 12am" or wakeup_time == "After 10am":
        tips.append(f"🌙 Sleep Earlier: Bed before 10 PM and up by 8 AM makes you super happy! Try reading a {book_type.split()[0].lower()} story first!")
    else:
        tips.append(f"💤 Great Sleep: Sleeping from {sleep_time} to {wakeup_time} is awesome! Add some calm music before bed!")

    if child_food == "Unhealthy":
        tips.append("🍎 Yummy Healthy Food: Swap burgers for fruits—it’s like magic for your smile!")
    elif child_food == "Healthy":
        tips.append("🥗 Super Eats: Your healthy food is cool! Add a fun veggie like carrots!")
    elif child_food == "Mixed":
        tips.append("🍽️ Food Mix: You’re half-healthy—add more fruits for extra energy!")

    if "Negative" in social_media_content and social_media_platforms:
        tips.append(f"🚫 Happy Scroll: Less yucky stuff on {social_media_platforms[0] if social_media_platforms else 'social media'}—follow fun pages instead!")
    elif social_media_platforms:
        tips.append(f"🌟 Fun Online: Watch cool {social_media_content[0].lower() if social_media_content else 'stuff'} on {social_media_platforms[0] if social_media_platforms else 'social media'}!")

    if "Very little" in family_time or "Mostly Negative" in home_environment:
        tips.append(f"👨‍👩‍👧 Family Fun: Play {hobbies[0].split()[0].lower() if hobbies else 'games'} with family—it’s a happiness boost!")
    else:
        tips.append(f"🏡 Family Rocks: Your {family_time.lower()} family time is great—keep it up with a fun day out!")

    if anxiety_level in ["Moderate", "High"]:
        tips.append(f"🧘 Relax Time: Breathe easy with {resources['Apps'][0].split(' - ')[0]}—it’s like a hug for your brain!")

    if len(tips) < 5:
        tips.append(f"🌈 Happy Moments: Do {hobbies[0].lower() if hobbies else 'drawing'} for 10 minutes—it’s super fun!")

    tips = list(dict.fromkeys(tips))[:6]

    recommendation_output = f"""
    <span style='font-size: 20px; font-weight: bold;'>🌈 Cool Stuff to Try</span>  
    <span style='font-size: 16px; font-weight: bold;'>Fun Apps</span>  
    {', '.join(resources['Apps'])}  
    <span style='font-size: 16px; font-weight: bold;'>Awesome Books</span>  
    {', '.join(resources['Books'])}  
    <span style='font-size: 16px; font-weight: bold;'>Neat Websites</span>  
    {', '.join(resources['Online Tools'])}<br><br>

    <span style='font-size: 20px; font-weight: bold;'>🎉 Super Tips for You:</span><br>  
    - {tips[0]}</span>  
    - {tips[1]}</span>  
    - {tips[2]}</span>  
    - {tips[3]}</span>  
    - {tips[4]}</span>  
    {f'- {tips[5]}' if len(tips) > 5 else ''}  
    """
    return recommendation_output

# def generate_pdf(depression_level, age, categorical_values, recommendations, 
#                  recommended_screen_time, child_screen_time, 
#                  recommended_tele_screen_time, child_tele_screen_time,
#                  mobile_graph_image, tele_graph_image):
#     buffer = BytesIO()
#     c = canvas.Canvas(buffer, pagesize=letter)
#     width, height = letter

#     # Helper function for multi-line text with proper spacing
#     def draw_wrapped_text(text, x, y, max_width, line_height=15):
#         words = text.split()
#         lines = []
#         current_line = []
        
#         for word in words:
#             test_line = ' '.join(current_line + [word])
#             if c.stringWidth(test_line, "Helvetica", 11) < max_width:
#                 current_line.append(word)
#             else:
#                 lines.append(' '.join(current_line))
#                 current_line = [word]
        
#         if current_line:
#             lines.append(' '.join(current_line))
        
#         for i, line in enumerate(lines):
#             c.drawString(x, y - (i * line_height), line)
        
#         return y - (len(lines) * line_height)

#     # Page 1: Header and Inputs
#     # Background
#     c.setFillColor(colors.HexColor('#E6F7FF'))  # Light blue background
#     c.rect(0, 0, width, height, fill=1)
    
#     # Header
#     c.setFillColor(colors.HexColor('#FFD966'))  # Yellow header
#     c.roundRect(30, height - 100, width - 60, 70, 15, fill=1, stroke=0)
#     c.setFont("Helvetica-Bold", 24)
#     c.setFillColor(colors.HexColor('#FF5252'))  # Red title
#     c.drawCentredString(width/2, height - 55, "🌟 Your Report 🌟")
#     c.setFont("Helvetica", 12)
#     c.setFillColor(colors.black)
#     c.drawCentredString(width/2, height - 80, f"Date: {pd.Timestamp.now().strftime('%d-%m-%Y')}")

#     # Inputs Section
#     c.setFillColor(colors.HexColor('#CCFFCC'))  # Light green background
#     c.roundRect(30, height - 320, width - 60, 200, 15, fill=1, stroke=0)
#     c.setFont("Helvetica-Bold", 18)
#     c.setFillColor(colors.HexColor('#673AB7'))  # Purple title
#     c.drawString(50, height - 150, "🎈 Your Cool Info!")
    
#     # First column
#     c.setFont("Helvetica-Bold", 12)
#     c.setFillColor(colors.HexColor('#3F51B5'))  # Dark blue
#     col1_x = 60
#     col1_y = height - 180
#     c.drawString(col1_x, col1_y, f"Age: {age}")
#     c.drawString(col1_x, col1_y - 25, f"You're a: {'Boy' if gender == 1 else 'Girl'}")
#     c.drawString(col1_x, col1_y - 50, f"Phone Time: {categorical_values.get('PHONE_SCREEN_TIME', '')}")
#     c.drawString(col1_x, col1_y - 75, f"TV Time: {categorical_values.get('TELEVISION_SCREEN_TIME', '')}")
    
#     # Second column
#     col2_x = width/2 + 30
#     col2_y = height - 180
#     c.drawString(col2_x, col2_y, f"Sleep: {categorical_values.get('SLEEPING_TIME', '')}")
#     c.drawString(col2_x, col2_y - 25, f"Wake Up: {categorical_values.get('WAKEUP_TIME', '')}")
    
#     # Hobbies with proper wrapping
#     hobbies_text = f"Fun Stuff: {categorical_values.get('HOBBIES', '')}"
#     if len(hobbies_text) > 40:
#         c.drawString(col2_x, col2_y - 50, "Fun Stuff:")
#         draw_wrapped_text(categorical_values.get('HOBBIES', ''), col2_x + 10, col2_y - 65, 200)
#     else:
#         c.drawString(col2_x, col2_y - 50, hobbies_text)
    
#     # Depression level indicator
#     c.setFont("Helvetica-Bold", 16)
#     level_color = colors.HexColor('#FF5252') if depression_level == "High" else \
#                  colors.HexColor('#FFC107') if depression_level == "Moderate" else \
#                  colors.HexColor('#4CAF50')
#     c.setFillColor(level_color)
#     c.drawString(width/2 - 100, height - 300, f"Your Depression Level: {depression_level}")
    
#     # Tips Section
#     c.setFillColor(colors.HexColor('#FFD6EC'))  # Light pink
#     c.roundRect(30, 30, width - 60, height - 370, 15, fill=1, stroke=0)
#     c.setFont("Helvetica-Bold", 18)
#     c.setFillColor(colors.HexColor('#2E7D32'))  # Dark green
#     c.drawString(50, height - 340, "🌈 Super Fun Tips!")
    
#     # Parse HTML recommendations and render properly
#     plain_text = BeautifulSoup(recommendations, "html.parser").get_text()
#     y_pos = height - 370
#     section_heading = None
#     tips_count = 0
    
#     for line in plain_text.split('\n'):
#         line = line.strip()
#         if not line:
#             continue
            
#         if "Cool Stuff to Try" in line or "Super Tips for You" in line:
#             continue
            
#         if "Fun Apps" in line:
#             c.setFont("Helvetica-Bold", 14)
#             c.setFillColor(colors.HexColor('#1976D2'))  # Blue heading
#             y_pos -= 30
#             c.drawString(60, y_pos, "🎮 Fun Apps:")
#             section_heading = "apps"
#             c.setFont("Helvetica", 11)
#             c.setFillColor(colors.black)
            
#         elif "Awesome Books" in line:
#             c.setFont("Helvetica-Bold", 14)
#             c.setFillColor(colors.HexColor('#1976D2'))  # Blue heading
#             y_pos -= 40
#             c.drawString(60, y_pos, "📚 Awesome Books:")
#             section_heading = "books"
#             c.setFont("Helvetica", 11)
#             c.setFillColor(colors.black)
            
#         elif "Neat Websites" in line:
#             c.setFont("Helvetica-Bold", 14)
#             c.setFillColor(colors.HexColor('#1976D2'))  # Blue heading
#             y_pos -= 40
#             c.drawString(60, y_pos, "🌐 Neat Websites:")
#             section_heading = "websites"
#             c.setFont("Helvetica", 11)
#             c.setFillColor(colors.black)
            
#         elif line.startswith("-"):
#             c.setFont("Helvetica", 11)
#             c.setFillColor(colors.black)
#             tips_count += 1
#             if tips_count > 3:  # Only show 3 tips on first page
#                 continue
                
#             y_pos -= 30
#             emoji = line[2:line.find(" ", 2)] if " " in line[2:] else ""
#             text = line[2 + len(emoji):].strip()
#             c.drawString(60, y_pos, emoji)
#             y_pos = draw_wrapped_text(text, 85, y_pos, width - 150)
            
#         elif section_heading:
#             y_pos -= 20
#             y_pos = draw_wrapped_text(line, 70, y_pos, width - 150)
            
#     # Page 2: Screen Time
#     c.showPage()
#     c.setFillColor(colors.HexColor('#E6F7FF'))  # Light blue background
#     c.rect(0, 0, width, height, fill=1)

#     # Header for page 2
#     c.setFillColor(colors.HexColor('#FFD966'))  # Yellow header
#     c.roundRect(30, height - 100, width - 60, 70, 15, fill=1, stroke=0)
#     c.setFont("Helvetica-Bold", 24)
#     c.setFillColor(colors.HexColor('#FF5252'))  # Red title
#     c.drawCentredString(width/2, height - 55, "📱 Screen Time Fun! 📺")
#     c.setFont("Helvetica", 12)
#     c.setFillColor(colors.black)
#     c.drawCentredString(width/2, height - 80, "Let's check your screen habits!")

#     # Phone Time Section
#     c.setFillColor(colors.HexColor('#E1F5FE'))  # Light blue background
#     c.roundRect(50, height - 350, width/2 - 70, 220, 15, fill=1, stroke=0)
#     c.setFont("Helvetica-Bold", 16)
#     c.setFillColor(colors.HexColor('#0277BD'))  # Dark blue title
#     c.drawString(70, height - 150, "📱 Phone Time")
    
#     # Phone time data
#     c.setFont("Helvetica-Bold", 12)
#     c.setFillColor(colors.HexColor('#01579B'))  # Dark blue
#     c.drawString(70, height - 180, f"Your Time: {child_screen_time} hrs")
    
#     c.setFillColor(colors.HexColor('#2E7D32'))  # Dark green
#     c.drawString(70, height - 200, f"Best Time: {recommended_screen_time} hrs")
    
#     # Status indicator for phone
#     phone_status = 'Too Much!' if child_screen_time > recommended_screen_time else \
#                   'Just Right' if abs(child_screen_time - recommended_screen_time) <= 0.5 else \
#                   'Great Job!'
#     status_color = colors.HexColor('#FF5252') if phone_status == 'Too Much!' else \
#                   colors.HexColor('#FFC107') if phone_status == 'Just Right' else \
#                   colors.HexColor('#4CAF50')
#     c.setFillColor(status_color)
#     c.drawString(70, height - 220, f"Status: {phone_status}")
    
#     # Display phone time graph
#     if mobile_graph_image:
#         c.drawImage(ImageReader(mobile_graph_image), 80, height - 330, width=180, height=90)

#     # TV Time Section
#     c.setFillColor(colors.HexColor('#FFF8E1'))  # Light yellow background
#     c.roundRect(width/2 + 20, height - 350, width/2 - 70, 220, 15, fill=1, stroke=0)
#     c.setFont("Helvetica-Bold", 16)
#     c.setFillColor(colors.HexColor('#FF6F00'))  # Orange title
#     c.drawString(width/2 + 40, height - 150, "📺 TV Time")
    
#     # TV time data
#     c.setFont("Helvetica-Bold", 12)
#     c.setFillColor(colors.HexColor('#E65100'))  # Dark orange
#     c.drawString(width/2 + 40, height - 180, f"Your Time: {child_tele_screen_time} hrs")
    
#     c.setFillColor(colors.HexColor('#2E7D32'))  # Dark green
#     c.drawString(width/2 + 40, height - 200, f"Best Time: {recommended_tele_screen_time} hrs")
    
#     # Status indicator for TV
#     tv_status = 'Too Much!' if child_tele_screen_time > recommended_tele_screen_time else \
#                'Just Right' if abs(child_tele_screen_time - recommended_tele_screen_time) <= 0.5 else \
#                'Great Job!'
#     status_color = colors.HexColor('#FF5252') if tv_status == 'Too Much!' else \
#                   colors.HexColor('#FFC107') if tv_status == 'Just Right' else \
#                   colors.HexColor('#4CAF50')
#     c.setFillColor(status_color)
#     c.drawString(width/2 + 40, height - 220, f"Status: {tv_status}")
    
#     # Display TV time graph
#     if tele_graph_image:
#         c.drawImage(ImageReader(tele_graph_image), width/2 + 50, height - 330, width=180, height=90)

#     # Continue to display remaining tips
#     c.setFillColor(colors.HexColor('#E0F7FA'))  # Light cyan
#     c.roundRect(50, 50, width - 100, height - 420, 15, fill=1, stroke=0)
#     c.setFont("Helvetica-Bold", 18)
#     c.setFillColor(colors.HexColor('#00695C'))  # Dark teal
#     c.drawString(70, height - 370, "🎉 More Awesome Tips")
    
#     # Parse HTML recommendations again for remaining tips
#     plain_text = BeautifulSoup(recommendations, "html.parser").get_text()
#     y_pos = height - 400
#     tips_count = 0
    
#     for line in plain_text.split('\n'):
#         line = line.strip()
#         if not line or not line.startswith("-"):
#             continue
            
#         tips_count += 1
#         if tips_count <= 3:  # Skip the tips we already showed on page 1
#             continue
            
#         c.setFont("Helvetica", 11)
#         c.setFillColor(colors.black)
#         y_pos -= 30
#         emoji = line[2:line.find(" ", 2)] if " " in line[2:] else ""
#         text = line[2 + len(emoji):].strip()
#         c.drawString(70, y_pos, emoji)
#         y_pos = draw_wrapped_text(text, 95, y_pos, width - 170)

#     # Personal message based on depression level
#     c.setFillColor(colors.HexColor('#FFECB3'))  # Light amber
#     c.roundRect(width/2 - 150, 80, 300, 80, 15, fill=1, stroke=0)
#     c.setFont("Helvetica-Bold", 14)
    
#     if depression_level == "High":
#         c.setFillColor(colors.HexColor('#D32F2F'))  # Dark red
#         message = "🚨 You might feel super sad. Let's play more and talk to a grown-up!"
#     elif depression_level == "Moderate":
#         c.setFillColor(colors.HexColor('#F57C00'))  # Dark amber
#         message = "⚠️ You're a bit sad. More fun outside can help!"
#     else:
#         c.setFillColor(colors.HexColor('#388E3C'))  # Dark green
#         message = "✅ You're super happy! Keep being awesome!"
        
#     draw_wrapped_text(message, width/2 - 130, 140, 260)
    
#     # Footer
#     c.setFont("Helvetica-Bold", 14)
#     c.setFillColor(colors.HexColor('#3F51B5'))  # Indigo
#     c.drawCentredString(width/2, 30, "Made just for YOU! Keep smiling! 😊")

#     c.save()
#     buffer.seek(0)
#     return buffer

# ----------------

def generate_pdf(depression_level, age, categorical_values, recommendations, 
                 recommended_screen_time, child_screen_time, 
                 recommended_tele_screen_time, child_tele_screen_time,
                 mobile_graph_image, tele_graph_image):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Helper function for multi-line text with proper spacing
    def draw_wrapped_text(text, x, y, max_width, line_height=15):
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            if c.stringWidth(test_line, "Helvetica", 11) < max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        for i, line in enumerate(lines):
            c.drawString(x, y - (i * line_height), line)
        
        return y - (len(lines) * line_height)

    # Page 1: Header and Inputs
    # Background
    c.setFillColor(colors.HexColor('#E6F7FF'))  # Light blue background
    c.rect(0, 0, width, height, fill=1)
    
    # Header
    c.setFillColor(colors.HexColor('#FFD966'))  # Yellow header
    c.roundRect(30, height - 100, width - 60, 70, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor('#FF5252'))  # Red title
    c.drawCentredString(width/2, height - 55, "🌟 Your Report 🌟")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height - 80, f"Date: {pd.Timestamp.now().strftime('%d-%m-%Y')}")

    # Inputs Section
    c.setFillColor(colors.HexColor('#CCFFCC'))  # Light green background
    c.roundRect(30, height - 320, width - 60, 200, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor('#673AB7'))  # Purple title
    c.drawString(50, height - 150, "🎈 Your Cool Info!")
    
    # First column
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#3F51B5'))  # Dark blue
    col1_x = 60
    col1_y = height - 180
    c.drawString(col1_x, col1_y, f"Age: {age}")
    c.drawString(col1_x, col1_y - 25, f"You're a: {'Boy' if gender == 1 else 'Girl'}")
    c.drawString(col1_x, col1_y - 50, f"Phone Time: {categorical_values.get('PHONE_SCREEN_TIME', '')}")
    c.drawString(col1_x, col1_y - 75, f"TV Time: {categorical_values.get('TELEVISION_SCREEN_TIME', '')}")
    
    # Second column
    col2_x = width/2 + 30
    col2_y = height - 180
    c.drawString(col2_x, col2_y, f"Sleep: {categorical_values.get('SLEEPING_TIME', '')}")
    c.drawString(col2_x, col2_y - 25, f"Wake Up: {categorical_values.get('WAKEUP_TIME', '')}")
    
    # Hobbies with proper wrapping
    hobbies_text = f"Fun Stuff: {categorical_values.get('HOBBIES', '')}"
    if len(hobbies_text) > 40:
        c.drawString(col2_x, col2_y - 50, "Fun Stuff:")
        draw_wrapped_text(categorical_values.get('HOBBIES', ''), col2_x + 10, col2_y - 65, 200)
    else:
        c.drawString(col2_x, col2_y - 50, hobbies_text)
    
    # Depression level indicator
    c.setFont("Helvetica-Bold", 16)
    level_color = colors.HexColor('#FF5252') if depression_level == "High" else \
                 colors.HexColor('#FFC107') if depression_level == "Moderate" else \
                 colors.HexColor('#4CAF50')
    c.setFillColor(level_color)
    c.drawString(width/2 - 100, height - 300, f"Your Depression Level: {depression_level}")
    
    # Tips Section
    c.setFillColor(colors.HexColor('#FFD6EC'))  # Light pink
    c.roundRect(30, 30, width - 60, height - 370, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor('#2E7D32'))  # Dark green
    # Move the title down inside the box
    c.drawString(50, height - 370, "🌈 Super Fun Tips!")
    
    # Parse HTML recommendations and render properly
    plain_text = BeautifulSoup(recommendations, "html.parser").get_text()
    y_pos = height - 380  # Start tips lower to accommodate title properly
    section_heading = None
    tips_count = 0
    
    for line in plain_text.split('\n'):
        line = line.strip()
        if not line:
            continue
            
        if "Cool Stuff to Try" in line or "Super Tips for You" in line:
            continue
            
        if "Fun Apps" in line:
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.HexColor('#1976D2'))  # Blue heading
            y_pos -= 30
            c.drawString(60, y_pos, "🎮 Fun Apps:")
            section_heading = "apps"
            c.setFont("Helvetica", 11)
            c.setFillColor(colors.black)
            
        elif "Awesome Books" in line:
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.HexColor('#1976D2'))  # Blue heading
            y_pos -= 40
            c.drawString(60, y_pos, "📚 Awesome Books:")
            section_heading = "books"
            c.setFont("Helvetica", 11)
            c.setFillColor(colors.black)
            
        elif "Neat Websites" in line:
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.HexColor('#1976D2'))  # Blue heading
            y_pos -= 40
            c.drawString(60, y_pos, "🌐 Neat Websites:")
            section_heading = "websites"
            c.setFont("Helvetica", 11)
            c.setFillColor(colors.black)
            
        elif line.startswith("-"):
            c.setFont("Helvetica", 11)
            c.setFillColor(colors.black)
            tips_count += 1
            if tips_count > 3:  # Only show 3 tips on first page
                continue
                
            y_pos -= 30
            emoji = line[2:line.find(" ", 2)] if " " in line[2:] else ""
            text = line[2 + len(emoji):].strip()
            c.drawString(60, y_pos, emoji)
            y_pos = draw_wrapped_text(text, 85, y_pos, width - 150)
            
        elif section_heading:
            y_pos -= 20
            y_pos = draw_wrapped_text(line, 70, y_pos, width - 150)
            
    # Page 2: Screen Time
    c.showPage()
    c.setFillColor(colors.HexColor('#E6F7FF'))  # Light blue background
    c.rect(0, 0, width, height, fill=1)

    # Header for page 2
    c.setFillColor(colors.HexColor('#FFD966'))  # Yellow header
    c.roundRect(30, height - 100, width - 60, 70, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor('#FF5252'))  # Red title
    c.drawCentredString(width/2, height - 55, "📱 Screen Time ! 📺")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height - 80, "Let's check your screen habits!")

    # Phone Time Section
    c.setFillColor(colors.HexColor('#C8E6C9'))  # Light green background
    c.roundRect(50, height - 350, width/2 - 70, 220, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor('#2E7D32'))  # Dark green title
    c.drawString(70, height - 150, "📱 Phone Time")
    
    # Phone time data
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#1B5E20'))  # Darker green
    c.drawString(70, height - 180, f"Your Time: {child_screen_time} hrs")
    
    c.setFillColor(colors.HexColor('#2E7D32'))  # Dark green
    c.drawString(70, height - 200, f"Best Time: {recommended_screen_time} hrs")
    
    # Status indicator for phone
    phone_status = 'Too Much!' if child_screen_time > recommended_screen_time else \
                  'Just Right' if abs(child_screen_time - recommended_screen_time) <= 0.5 else \
                  'Great Job!'
    status_color = colors.HexColor('#FF5252') if phone_status == 'Too Much!' else \
                  colors.HexColor('#FFC107') if phone_status == 'Just Right' else \
                  colors.HexColor('#4CAF50')
    c.setFillColor(status_color)
    c.drawString(70, height - 220, f"Status: {phone_status}")
    
    # Display phone time graph
    if mobile_graph_image:
        c.drawImage(ImageReader(mobile_graph_image), 80, height - 330, width=180, height=90)

    # TV Time Section
    c.setFillColor(colors.HexColor('#FFF8E1'))  # Light yellow background
    c.roundRect(width/2 + 20, height - 350, width/2 - 70, 220, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor('#FF6F00'))  # Orange title
    c.drawString(width/2 + 40, height - 150, "📺 TV Time")
    
    # TV time data
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#E65100'))  # Dark orange
    c.drawString(width/2 + 40, height - 180, f"Your Time: {child_tele_screen_time} hrs")
    
    c.setFillColor(colors.HexColor('#2E7D32'))  # Dark green
    c.drawString(width/2 + 40, height - 200, f"Best Time: {recommended_tele_screen_time} hrs")
    
    # Status indicator for TV
    tv_status = 'Too Much!' if child_tele_screen_time > recommended_tele_screen_time else \
               'Just Right' if abs(child_tele_screen_time - recommended_tele_screen_time) <= 0.5 else \
               'Great Job!'
    status_color = colors.HexColor('#FF5252') if tv_status == 'Too Much!' else \
                  colors.HexColor('#FFC107') if tv_status == 'Just Right' else \
                  colors.HexColor('#4CAF50')
    c.setFillColor(status_color)
    c.drawString(width/2 + 40, height - 220, f"Status: {tv_status}")
    
    # Display TV time graph
    if tele_graph_image:
        c.drawImage(ImageReader(tele_graph_image), width/2 + 50, height - 330, width=180, height=90)

    # FIXED: Create clearly separated regions with proper spacing
    
    # Tips Section - Made smaller to leave space for the message box below
    c.setFillColor(colors.HexColor('#FFCCBC'))  # Light peach
    c.roundRect(50, 200, width - 100, height - 570, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor('#BF360C'))  # Dark red-orange
    c.drawString(70, height - 390, "🎉 More Awesome Tips")
    
    # Parse HTML recommendations again for remaining tips
    plain_text = BeautifulSoup(recommendations, "html.parser").get_text()
    y_pos = height - 400
    tips_count = 0
    
    for line in plain_text.split('\n'):
        line = line.strip()
        if not line or not line.startswith("-"):
            continue
            
        tips_count += 1
        if tips_count <= 3:  # Skip the tips we already showed on page 1
            continue
            
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)
        y_pos -= 30
        emoji = line[2:line.find(" ", 2)] if " " in line[2:] else ""
        text = line[2 + len(emoji):].strip()
        c.drawString(70, y_pos, emoji)
        y_pos = draw_wrapped_text(text, 95, y_pos, width - 170)

    # Personal message - FIXED: Clearly separated from tips section
    c.setFillColor(colors.HexColor('#FFECB3'))  # Light amber
    c.roundRect(width/2 - 150, 100, 300, 80, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 14)
    
    if depression_level == "High":
        c.setFillColor(colors.HexColor('#D32F2F'))  # Dark red
        message = "🚨 Talk to a grown-up about feeling sad"
    elif depression_level == "Moderate":
        c.setFillColor(colors.HexColor('#F57C00'))  # Dark amber
        message = "⚠️ Try playing outside more"
    else:
        c.setFillColor(colors.HexColor('#388E3C'))  # Dark green
        message = "✅ Keep being awesome!"
        
    # Draw the emoji separately    
    c.drawString(width/2 - 130, 160, emoji)
    draw_wrapped_text(message, width/2 - 110, 160, 240)
    
    # Footer
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor('#3F51B5'))  # Indigo
    c.drawCentredString(width/2, 30, "Made just for YOU! Keep smiling! 😊")

    c.save()
    buffer.seek(0)
    return buffer


# -------------------

# Prediction button
if st.button("Predict Depression Level"):
    input_scaled = scaler.transform(input_data)
    prediction = rf_model.predict(input_scaled)
    
    depression_level = prediction[0]
    st.subheader(f"Predicted Depression Level: **{depression_level}**")
    
    recommendations = get_custom_recommendations(
        depression_level, age, input_data, categorical_values, 
        child_screen_time, child_tele_screen_time, 
        recommended_screen_time, recommended_tele_screen_time, child_food
    )
    st.markdown(recommendations, unsafe_allow_html=True)

    # Mobile Screen Time Visualization
    threshold = 0.1 * recommended_screen_time
    bar_color = ('red' if child_screen_time > recommended_screen_time else 
                 'yellow' if abs(child_screen_time - recommended_screen_time) <= threshold else 'green')
    zone_label = 'Alert Zone' if bar_color == 'red' else 'Caution Zone' if bar_color == 'yellow' else 'Safe Zone'

    fig_mobile, ax_mobile = plt.subplots(figsize=(4, 4), dpi=100)
    bar_width = 0.4
    max_y = max(child_screen_time, recommended_screen_time) * 1.5

    safe_upper = recommended_screen_time - threshold
    caution_upper = recommended_screen_time + threshold
    ax_mobile.axhspan(0, safe_upper, facecolor='green', alpha=0.1, zorder=0)
    ax_mobile.axhspan(safe_upper, caution_upper, facecolor='yellow', alpha=0.1, zorder=0)
    ax_mobile.axhspan(caution_upper, max_y, facecolor='red', alpha=0.1, zorder=0)

    bar = ax_mobile.bar(['Phone Time'], [child_screen_time], color=bar_color, width=bar_width)
    ax_mobile.text(0.05, 0.95, f'Best ({recommended_screen_time} hr)', 
                   transform=ax_mobile.transAxes, fontsize=10, va='top', ha='left', color='green')
    ax_mobile.set_ylabel("Hours")
    ax_mobile.set_title(f"Phone Time: {zone_label}")
    ax_mobile.set_ylim(0, max_y)
    ax_mobile.set_yticks(range(0, int(max_y) + 1, 1))
    ax_mobile.text(0, child_screen_time + 0.05, f'{child_screen_time} hr', ha='center', va='bottom')
    x_pos = bar_width / 2 + 0.05
    ax_mobile.text(x_pos, safe_upper / 2, 'Safe', color='green', ha='left', va='center')
    ax_mobile.text(x_pos, (safe_upper + caution_upper) / 2, 'Careful', color='yellow', ha='left', va='center')
    ax_mobile.text(x_pos, (caution_upper + max_y) / 2, 'Whoa!', color='red', ha='left', va='center')
    ax_mobile.set_xlim(-0.5, 1.5)
    plt.tight_layout()
    st.pyplot(fig_mobile)

    mobile_graph_image = BytesIO()
    fig_mobile.savefig(mobile_graph_image, format='png', bbox_inches='tight')
    mobile_graph_image.seek(0)

    # TV Screen Time Visualization
    threshold = 0.1 * recommended_tele_screen_time
    bar_color = ('red' if child_tele_screen_time > recommended_tele_screen_time else 
                 'yellow' if abs(child_tele_screen_time - recommended_tele_screen_time) <= threshold else 'green')
    zone_label = 'Alert Zone' if bar_color == 'red' else 'Caution Zone' if bar_color == 'yellow' else 'Safe Zone'

    fig_tele, ax_tele = plt.subplots(figsize=(4, 4), dpi=100)
    bar_width = 0.4
    max_y = max(child_tele_screen_time, recommended_tele_screen_time) * 1.5

    safe_upper = recommended_tele_screen_time - threshold
    caution_upper = recommended_tele_screen_time + threshold
    ax_tele.axhspan(0, safe_upper, facecolor='green', alpha=0.1, zorder=0)
    ax_tele.axhspan(safe_upper, caution_upper, facecolor='yellow', alpha=0.1, zorder=0)
    ax_tele.axhspan(caution_upper, max_y, facecolor='red', alpha=0.1, zorder=0)

    bar = ax_tele.bar(['TV Time'], [child_tele_screen_time], color=bar_color, width=bar_width)
    ax_tele.text(0.05, 0.95, f'Best ({recommended_tele_screen_time} hr)', 
                 transform=ax_tele.transAxes, fontsize=10, va='top', ha='left', color='green')
    ax_tele.set_ylabel("Hours")
    ax_tele.set_title(f"TV Time: {zone_label}")
    ax_tele.set_ylim(0, max_y)
    ax_tele.set_yticks(range(0, int(max_y) + 1, 1))
    ax_tele.text(0, child_tele_screen_time + 0.05, f'{child_tele_screen_time} hr', ha='center', va='bottom')
    x_pos = bar_width / 2 + 0.05
    ax_tele.text(x_pos, safe_upper / 2, 'Safe', color='green', ha='left', va='center')
    ax_tele.text(x_pos, (safe_upper + caution_upper) / 2, 'Careful', color='yellow', ha='left', va='center')
    ax_tele.text(x_pos, (caution_upper + max_y) / 2, 'Whoa!', color='red', ha='left', va='center')
    ax_tele.set_xlim(-0.5, 1.5)
    plt.tight_layout()
    st.pyplot(fig_tele)

    tele_graph_image = BytesIO()
    fig_tele.savefig(tele_graph_image, format='png', bbox_inches='tight')
    tele_graph_image.seek(0)

    if depression_level == "High":
        st.warning("🚨 You might feel super sad. Let’s play more and talk to a grown-up!")
    elif depression_level == "Moderate":
        st.info("⚠️ You’re a bit sad. More fun outside can help!")
    else:
        st.success("✅ You’re super happy! Keep being awesome!")

    pdf_buffer = generate_pdf(
        depression_level, age, categorical_values, recommendations,
        recommended_screen_time, child_screen_time,
        recommended_tele_screen_time, child_tele_screen_time,
        mobile_graph_image, tele_graph_image
    )
    st.download_button(
        label="Download Your Report!",
        data=pdf_buffer,
        file_name="happiness_report.pdf",
        mime="application/pdf"
    )
