import streamlit as st
import pandas as pd
import numpy as np
import joblib
import sklearn
from sklearn.preprocessing import StandardScaler
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
from PyPDF2 import PdfMerger, PdfReader
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

# Configure page settings
st.set_page_config(page_title="Model & Report Generation", layout="wide", page_icon="📄")

# Initialize variables to None
rf_model = None
scaler = None
trained_features = None

# Load trained model, scaler, and features
BASE_PATH = "D:/ALL CODE/"
MODEL_FILE = os.path.join(BASE_PATH, "RANDOM_FOREST_MODEL.pkl")
SCALER_FILE = os.path.join(BASE_PATH, "SCALER.pkl")
FEATURES_FILE = os.path.join(BASE_PATH, "TRAINED_FEATURES.pkl")

# Check if files exist
for file_path in [MODEL_FILE, SCALER_FILE, FEATURES_FILE]:
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        st.stop()

try:
    rf_model = joblib.load(MODEL_FILE)
    scaler = joblib.load(SCALER_FILE)
    trained_features = joblib.load(FEATURES_FILE)
    if isinstance(trained_features, pd.Index):
        trained_features = trained_features.tolist()
    if not isinstance(trained_features, (list, tuple)):
        raise ValueError("trained_features must be a list or tuple of feature names")
    print("Trained features:", trained_features)
except Exception as e:
    st.error(f"Error loading files: {e}")
    st.error(
        """
        This error likely indicates a version mismatch between the scikit-learn version used to train the model 
        and your current version ({sklearn.__version__}). To fix this:
        1. Install the scikit-learn version used to train the model (e.g., `pip install scikit-learn==1.2.2`).
        2. Or retrain the model with your current version and update the pickle files.
        """
    )
    st.stop()

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
    'REPLICATE_SOCIAL_MEDIA': ['Low', 'Moderate', 'High'],
    'Family Communication Style': ['Low Communication', 'Moderate Communication', 'High Communication'],
    'Emotional Support Level': ['Low', 'Moderate', 'High'],
    'Child Stress Level': ['Low', 'Moderate', 'High'],
    'Family Quality Time': ['Low', 'Moderate', 'High'],
    'Personal Interest Development': ['Low', 'Moderate', 'High']
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
    <span style='font-size: 20px; font-weight: bold;'>🌈 Cool Stuff to Try</span><br>  
    <span style='font-size: 16px; font-weight: bold;'>Fun Apps</span>  
    {', '.join(resources['Apps'])}<br>  
    <span style='font-size: 16px; font-weight: bold;'>Awesome Books</span>  
    {', '.join(resources['Books'])}<br>  
    <span style='font-size: 16px; font-weight: bold;'>Neat Websites</span> 
    {', '.join(resources['Online Tools'])}<br>
    <br><span style='font-size: 20px; font-weight: bold;'>🎉 Super Tips for You:</span><br>  
    - {tips[0]}</span>  
    - {tips[1]}</span>  
    - {tips[2]}</span>  
    - {tips[3]}</span>  
    - {tips[4]}</span>  
    {f'- {tips[5]}' if len(tips) > 5 else ''}  
    """

    # Generate Mental Health Insights
    mental_health_insights = generate_mental_health_insights(categorical_values)
    
    # Extend recommendations with mental health insights
    recommendation_output = extend_recommendations(recommendation_output, mental_health_insights)
    
    # Generate Mental Health Visualization
    mental_health_graph = create_mental_health_visualization(categorical_values)

    return recommendation_output, mental_health_graph

def generate_mental_health_insights(categorical_values):
    insights = {
        "Communication": [],
        "Emotional Support": [],
        "Potential Interventions": []
    }
    
    family_communication = categorical_values.get('Family Communication Style', '')
    if family_communication == "Low Communication":
        insights["Communication"].append("🗣️ Improve Family Dialogue: Practice daily check-ins, create a safe space for open conversations.")
        insights["Potential Interventions"].append("Consider family counseling sessions to enhance communication skills.")
    elif family_communication == "Moderate Communication":
        insights["Communication"].append("👥 Good Communication Foundation: Continue encouraging honest discussions.")
    else:
        insights["Communication"].append("💖 Excellent Communication: Keep nurturing your open family dialogue.")
    
    emotional_support = categorical_values.get('Emotional Support Level', '')
    if emotional_support == "Low":
        insights["Emotional Support"].append("❤️ Boost Emotional Connections: Spend more quality time, show empathy and active listening.")
        insights["Potential Interventions"].append("Explore child psychology workshops to understand emotional nurturing.")
    elif emotional_support == "Moderate":
        insights["Emotional Support"].append("🤗 Good Emotional Foundation: Continue showing love and understanding.")
    else:
        insights["Emotional Support"].append("🌟 Strong Emotional Bond: Your support is making a positive difference!")
    
    stress_level = categorical_values.get('Child Stress Level', 'Low')
    if stress_level == "High":
        insights["Potential Interventions"].append("🧘 Stress Management: Introduce mindfulness techniques, consider professional counseling.")
    
    return insights

def create_mental_health_visualization(categorical_values):
    plt.figure(figsize=(8, 6))
    categories = [
        'Communication',
        'Emotional Support', 
        'Stress Management',
        'Family Bonding',
        'Personal Interests'
    ]
    
    def get_score(category):
        mapping = {
            'Low': 1, 
            'Moderate': 2, 
            'High': 3,
            'Low Communication': 1,
            'Moderate Communication': 2,
            'High Communication': 3
        }
        value = categorical_values.get(category, 'Low')
        return mapping.get(value, 1)
    
    values = [
        get_score('Family Communication Style'),
        get_score('Emotional Support Level'),
        get_score('Child Stress Level'),
        get_score('Family Quality Time'),
        get_score('Personal Interest Development')
    ]
    
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
    values = np.concatenate((values, [values[0]]))
    angles = np.concatenate((angles, [angles[0]]))
    
    plt.polar(angles, values, 'o-', linewidth=2)
    plt.fill(angles, values, alpha=0.25)
    plt.xticks(angles[:-1], categories)
    plt.title('Mental Health Wellness Radar')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    
    return buffer

def extend_recommendations(recommendations, mental_health_insights):
    additional_recommendations = "\n\n<span style='font-size: 20px; font-weight: bold;'>🌈 Mental Health Insights</span>\n"
    
    for category, insights in mental_health_insights.items():
        additional_recommendations += f"\n<span style='font-size: 16px; font-weight: bold;'>{category} Insights:</span>\n"
        for insight in insights:
            additional_recommendations += f"- {insight}\n"
    
    return recommendations + additional_recommendations

def generate_pdf(depression_level, age, categorical_values, recommendations, 
                 recommended_screen_time, child_screen_time, 
                 recommended_tele_screen_time, child_tele_screen_time,
                 mobile_graph_image, tele_graph_image, mental_health_graph,
                 gender=None):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from io import BytesIO
    from bs4 import BeautifulSoup
    import pandas as pd
    import os

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    use_emoji_font = False
    font_path = "NotoColorEmoji.ttf"
    try:
        pdfmetrics.registerFont(TTFont('SegoeUIEmoji', 'seguiemj.ttf'))
        use_emoji_font = True
    except Exception as e:
        print(f"Warning: Could not load Segoe UI Emoji font: {e}")
        if os.path.exists(font_path):
            try:
                pdfmetrics.registerFont(TTFont('NotoColorEmoji', font_path))
                use_emoji_font = True
            except Exception as e:
                print(f"Warning: Could not load NotoColorEmoji font: {e}")
        else:
            print("Warning: NotoColorEmoji.ttf not found. Falling back to emoji replacement.")

    def draw_wrapped_text(text, x, y, max_width, min_y, line_height=15, font_size=11, emoji=False):
        if emoji and use_emoji_font:
            c.setFont("SegoeUIEmoji" if 'SegoeUIEmoji' in pdfmetrics.getRegisteredFontNames() else "NotoColorEmoji", font_size)
        else:
            c.setFont("Helvetica", font_size)
            if not use_emoji_font and emoji:
                text = replace_emojis(text)
        
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            font_name = "SegoeUIEmoji" if emoji and use_emoji_font and 'SegoeUIEmoji' in pdfmetrics.getRegisteredFontNames() else \
                        "NotoColorEmoji" if emoji and use_emoji_font else "Helvetica"
            if c.stringWidth(test_line, font_name, font_size) < max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        new_y = y
        for i, line in enumerate(lines):
            if new_y - (i * line_height) > min_y:
                c.drawString(x, new_y - (i * line_height), line)
            else:
                return new_y - (i * line_height), True
        return new_y - (len(lines) * line_height), False

    def replace_emojis(text):
        emoji_map = {
            '🌟': '*', '🎂': '(Age)', '👦': '(Boy)', '👧': '(Girl)', 
            '📱': '(Phone)', '📺': '(TV)', '😴': '(Sleep)', '🌞': '(Wakeup)', 
            '🎨': '(Hobby)', '💖': '(Mood)', '🌈': '(Tips)', '📊': '(Report)',
            '🧠': '(Mind)', '🗣️': '(Talk)', '❤️': '(Heart)', '🧘': '(Calm)'
        }
        for emoji, replacement in emoji_map.items():
            text = text.replace(emoji, replacement)
        return text

    c.setFillColor(colors.HexColor('#E6F7FF'))
    c.rect(0, 0, width, height, fill=1)
    
    c.setFillColor(colors.HexColor('#FFD966'))
    c.roundRect(30, height - 100, width - 60, 70, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor('#FF5252'))
    c.drawCentredString(width/2, height - 55, "🤗 Your Mental Health Report 🤗")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height - 80, f"Date: {pd.Timestamp.now().strftime('%d-%m-%Y')}")

    c.setFillColor(colors.HexColor('#CCFFCC'))
    c.roundRect(30, height - 320, width - 60, 200, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor('#673AB7'))
    c.drawString(50, height - 150, "Your Cool Info! 🌟")
    
    col1_x, col1_y = 60, height - 180
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#3F51B5'))
    c.drawString(col1_x, col1_y, f"Age: {age}")
    c.drawString(col1_x, col1_y - 25, f"You're a: {'Boy 👦' if gender == 1 else 'Girl 👧'}")
    c.drawString(col1_x, col1_y - 50, f"Mobile Time: {categorical_values.get('PHONE_SCREEN_TIME', '')} 📱")
    c.drawString(col1_x, col1_y - 75, f"TV Time: {categorical_values.get('TELEVISION_SCREEN_TIME', '')} 📺")

    col2_x, col2_y = width/2 + 30, height - 180
    c.drawString(col2_x, col2_y, f"Sleep: {categorical_values.get('SLEEPING_TIME', '')} 😴")
    c.drawString(col2_x, col2_y - 25, f"Wake Up: {categorical_values.get('WAKEUP_TIME', '')} 🌞")
    c.drawString(col2_x, col2_y - 50, "Hobbies: 🎨")
    draw_wrapped_text(categorical_values.get('HOBBIES', ''), col2_x + 10, col2_y - 65, width - col2_x - 40, col2_y - 120)

    c.setFont("Helvetica-Bold", 16)
    level_color = colors.HexColor('#FF5252') if depression_level == "High" else \
                 colors.HexColor('#FFC107') if depression_level == "Moderate" else \
                 colors.HexColor('#4CAF50')
    c.setFillColor(level_color)
    c.drawString(width/2 - 100, height - 300, f"Your Depression Level: {depression_level} 💖")

    c.setFillColor(colors.HexColor('#FFD6EC'))
    c.roundRect(30, 30, width - 60, height - 370, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor('#2E7D32'))
    c.drawString(50, height - 370, "Super Fun Tips! 🌈")

    plain_text = BeautifulSoup(recommendations, "html.parser").get_text()
    y_pos = height - 400
    tips_count = 0
    section_heading = None

    for line in plain_text.split('\n'):
        line = line.strip()
        if not line:
            continue

        if "Cool Stuff to Try" in line or "Mental Health Insights" in line:
            continue

        if "Fun Apps" in line:
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.HexColor('#1976D2'))
            y_pos -= 20
            c.drawString(60, y_pos, "Fun Apps:")
            section_heading = "apps"
            c.setFont("Helvetica", 11)
            c.setFillColor(colors.black)

        elif "Awesome Books" in line:
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.HexColor('#1976D2'))
            y_pos -= 30
            c.drawString(60, y_pos, "Awesome Books:")
            section_heading = "books"
            c.setFont("Helvetica", 11)
            c.setFillColor(colors.black)

        elif "Neat Websites" in line:
            c.setFont("Helvetica-Bold", 14)
            c.setFillColor(colors.HexColor('#1976D2'))
            y_pos -= 30
            c.drawString(60, y_pos, "Neat Websites:")
            section_heading = "websites"
            c.setFont("Helvetica", 11)
            c.setFillColor(colors.black)

        elif line.startswith("-"):
            c.setFont("Helvetica", 11)
            c.setFillColor(colors.black)
            tips_count += 1
            if tips_count > 3:
                continue
            y_pos -= 20
            text = line[2:].strip()
            y_pos, overflow = draw_wrapped_text(text, 60, y_pos, width - 100, 40, emoji=True)
            if overflow:
                break

        elif section_heading:
            y_pos -= 15
            y_pos, overflow = draw_wrapped_text(line, 70, y_pos, width - 110, 40)
            if overflow:
                break

    c.showPage()
    c.setFillColor(colors.HexColor('#E6F7FF'))
    c.rect(0, 0, width, height, fill=1)

    c.setFillColor(colors.HexColor('#FFD966'))
    c.roundRect(30, height - 100, width - 60, 70, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor('#FF5252'))
    c.drawCentredString(width/2, height - 55, "Screen Time! 📱📺")
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawCentredString(width/2, height - 80, "Let's check your screen habits!")

    c.setFillColor(colors.HexColor('#C8E6C9'))
    c.roundRect(50, height - 350, width/2 - 70, 220, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor('#2E7D32'))
    c.drawString(70, height - 150, "Mobile Time 📱")

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#1B5E20'))
    c.drawString(70, height - 180, f"Your Time: {child_screen_time} hrs")
    c.setFillColor(colors.HexColor('#2E7D32'))
    c.drawString(70, height - 200, f"Best Time: {recommended_screen_time} hrs")

    phone_status = 'Too Much!' if child_screen_time > recommended_screen_time else 'Great Job!'
    status_color = colors.HexColor('#FF5252') if phone_status == 'Too Much!' else colors.HexColor('#4CAF50')
    c.setFillColor(status_color)
    c.drawString(70, height - 220, f"Status: {phone_status}")

    if mobile_graph_image:
        c.drawImage(ImageReader(mobile_graph_image), 80, height - 330, width=180, height=90)

    c.setFillColor(colors.HexColor('#FFF8E1'))
    c.roundRect(width/2 + 20, height - 350, width/2 - 70, 220, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 16)
    c.setFillColor(colors.HexColor('#FF6F00'))
    c.drawString(width/2 + 40, height - 150, "TV Time 📺")

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(colors.HexColor('#E65100'))
    c.drawString(width/2 + 40, height - 180, f"Your Time: {child_tele_screen_time} hrs")
    c.setFillColor(colors.HexColor('#2E7D32'))
    c.drawString(width/2 + 40, height - 200, f"Best Time: {recommended_tele_screen_time} hrs")

    tv_status = 'Too Much!' if child_tele_screen_time > recommended_tele_screen_time else 'Great Job!'
    status_color = colors.HexColor('#FF5252') if tv_status == 'Too Much!' else colors.HexColor('#4CAF50')
    c.setFillColor(status_color)
    c.drawString(width/2 + 40, height - 220, f"Status: {tv_status}")

    if tele_graph_image:
        c.drawImage(ImageReader(tele_graph_image), width/2 + 50, height - 330, width=180, height=90)

    c.setFillColor(colors.HexColor('#FFCCBC'))
    c.roundRect(50, 50, width - 100, height - 400, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor('#BF360C'))
    c.drawString(70, height - 420, "More Awesome Tips 🌈")

    y_pos = height - 450
    tips_count = 0
    for line in plain_text.split('\n'):
        line = line.strip()
        if not line or not line.startswith("-"):
            continue
        tips_count += 1
        if tips_count <= 3:
            continue
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)
        y_pos -= 20
        text = line[2:].strip()
        y_pos, overflow = draw_wrapped_text(text, 80, y_pos, width - 160, 60, emoji=True)
        if overflow:
            break

    c.showPage()
    c.setFillColor(colors.HexColor('#E6F7FF'))
    c.rect(0, 0, width, height, fill=1)

    c.setFillColor(colors.HexColor('#FFD966'))
    c.roundRect(30, height - 100, width - 60, 70, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor('#FF5252'))
    c.drawCentredString(width/2, height - 55, "Mental Health Insights 🧠")

    y_pos = height - 150
    mental_health_insights = generate_mental_health_insights(categorical_values)
    for category, insights in mental_health_insights.items():
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.HexColor('#1976D2'))
        y_pos -= 30
        c.drawString(50, y_pos, f"{category} Insights:")
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)
        for insight in insights:
            y_pos -= 20
            y_pos, overflow = draw_wrapped_text(insight, 60, y_pos, width - 120, 50, emoji=True)
            if overflow:
                c.showPage()
                c.setFillColor(colors.HexColor('#E6F7FF'))
                c.rect(0, 0, width, height, fill=1)
                y_pos = height - 50

    y_pos -= 40
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(colors.HexColor('#388E3C'))
    c.drawString(50, y_pos, "Mental Health Resources")

    resources = [
        ("Mental Health & Well-Being", [
            "1. Child Mind Institute – https://childmind.org - Expert advice on children's mental health, screen time, and emotional well-being.",
            "2. Common Sense Media – https://www.commonsensemedia.org - Provides age-appropriate content recommendations and tips on managing screen time.",
            "3. American Academy of Pediatrics (HealthyChildren.org) – https://www.healthychildren.org - Research-backed parenting advice, including media use guidelines.",
            "4. The National Institute of Mental Health (NIMH) – https://www.nimh.nih.gov - Information on child mental health, anxiety, and depression."
        ]),
        ("Educational & Safe Content Platforms", [
            "5. PBS Kids – https://pbskids.org - Interactive games, videos, and activities that support child development.",
            "6. National Geographic Kids – https://kids.nationalgeographic.com - Engaging articles, videos, and fun educational content.",
            "7. BBC Bitesize – https://www.bbc.co.uk/bitesize - Free online learning resources for children of different age groups.",
            "8. Khan Academy Kids – https://www.khanacademy.org/kids - Free educational games and lessons for young learners."
        ]),
        ("Managing Screen Time & Digital Well-Being", [
            "9. Screen Time Guidelines by WHO – https://www.who.int/news-room/q-a-detail/children-and-digital-media - Official recommendations on screen time for children.",
            "10. Google Family Link – https://families.google.com/familylink/ - A parental control app for managing children’s digital activity.",
            "11. Wait Until 8th – https://www.waituntil8th.org - Encourages delaying smartphone use in young children."
        ]),
        ("Eye Health & Blue Light Protection", [
            "12. The Vision Council (Digital Eye Strain Guide) – https://thevisioncouncil.org/content/digital-eye-strain - Guide on preventing eye strain from screen exposure.",
            "13. American Optometric Association – https://www.aoa.org/healthy-eyes - Tips on maintaining healthy vision for children.",
            "14. Blue Light & Sleep – Sleep Foundation – https://www.sleepfoundation.org/how-sleep-works/light-exposure - How screen exposure affects sleep and how to improve sleep habits."
        ])
    ]

    y_pos -= 30
    for category, items in resources:
        c.setFont("Helvetica-Bold", 16)
        c.setFillColor(colors.HexColor('#388E3C'))
        y_pos -= 25
        y_pos, _ = draw_wrapped_text(category, 50, y_pos, width - 100, 50, line_height=20, font_size=14)
        c.setFont("Helvetica", 11)
        c.setFillColor(colors.black)
        for item in items:
            y_pos -= 15
            y_pos, overflow = draw_wrapped_text(item, 60, y_pos, width - 120, 50)
            if overflow:
                c.showPage()
                c.setFillColor(colors.HexColor('#E6F7FF'))
                c.rect(0, 0, width, height, fill=1)
                y_pos = height - 50
                c.setFont("Helvetica", 11)
                c.setFillColor(colors.black)

    c.showPage()
    c.setFillColor(colors.HexColor('#E6F7FF'))
    c.rect(0, 0, width, height, fill=1)

    c.setFillColor(colors.HexColor('#FFD966'))
    c.roundRect(30, height - 100, width - 60, 70, 15, fill=1, stroke=0)
    c.setFont("Helvetica-Bold", 24)
    c.setFillColor(colors.HexColor('#FF5252'))
    c.drawCentredString(width/2, height - 55, "Mental Health Wellness Radar 📊")

    if mental_health_graph:
        c.drawImage(ImageReader(mental_health_graph), 50, height - 550, width=500, height=400)

    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)
    description = (
        "This radar shows your happiness! Big points mean you're great at that part, "
        "smaller ones mean a little boost could help."
    )
    draw_wrapped_text(description, 50, height - 570, width - 100, 50)

    c.save()
    buffer.seek(0)
    return buffer

def send_email_report(email_address, pdf_buffer, child_name):
    """Send PDF report via email using Gmail SMTP"""
    try:
        # Gmail SMTP configuration
        HOST = "smtp.gmail.com"
        PORT = 587
        FROM_EMAIL = "praaadhindu@gmail.com"  # Replace with your Gmail email
        PASSWORD = "tbkoxysgkoofetcx"  # Replace with your Gmail app-specific password
        TO_EMAIL = email_address

        # Create email message
        message = MIMEMultipart("alternative")
        message['Subject'] = f"Feelings Puzzle Report - {child_name}"
        message['From'] = FROM_EMAIL
        message['To'] = TO_EMAIL

        # Email body (HTML)
        html = f"""
        <html>
        <body>
            <p>Hello,</p>
            <p>Attached is the Feelings Puzzle report for {child_name}.</p>
            <p>This report provides insights into how {child_name} is feeling and experiencing emotions.</p>
            <p>Thank you for using Feelings Puzzle!</p>
        </body>
        </html>
        """
        html_part = MIMEText(html, 'html')
        message.attach(html_part)

        # Attach PDF
        pdf_attachment = MIMEApplication(pdf_buffer.read(), _subtype="pdf")
        pdf_buffer.seek(0)
        pdf_attachment.add_header('Content-Disposition', f'attachment; filename=feelings_puzzle_{child_name}.pdf')
        message.attach(pdf_attachment)

        # Set up SMTP connection
        smtp = smtplib.SMTP(HOST, PORT)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(FROM_EMAIL, PASSWORD)
        smtp.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())
        smtp.quit()

        return True, "Email sent successfully!"
    except Exception as e:
        return False, str(e)

# Prediction button
if st.button("Predict Depression Level"):
    input_scaled = scaler.transform(input_data)
    prediction = rf_model.predict(input_scaled)
    
    depression_level = prediction[0]
    st.subheader(f"Predicted Depression Level: **{depression_level}**")
    
    recommendations, mental_health_graph = get_custom_recommendations(
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

    # Display Mental Health Visualization
    st.subheader("Mental Health Wellness Radar")
    st.markdown(
        """
        Here’s what your child’s **Mental Health Wellness Radar** shows: Each point represents a key part of their happiness. 
        A big stretch toward **Communication** means they’re great at sharing with family, while a shorter one might suggest 
        more family talks could help. A far-out **Emotional Support** point shows they feel loved, but a smaller one could 
        mean they need extra hugs. **Stress Management** stretching wide means they handle worries well—if it’s close to 
        the center, they might need calming tricks. A long **Family Bonding** line shows awesome together-time, and a big 
        **Personal Interests** point means their hobbies are thriving! Check the shape to see their strengths and where a 
        little boost could make them shine even more.
        """
    )
    st.image(mental_health_graph, width=600)

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
        mobile_graph_image, tele_graph_image, mental_health_graph,
        gender=gender
    )
    st.download_button(
        label="Download Your Report!",
        data=pdf_buffer,
        file_name="happiness_report.pdf",
        mime="application/pdf"
    )
     # Store the pdf_buffer in session state so it's available after page rerun
    st.session_state.pdf_buffer = pdf_buffer
    st.session_state.report_generated = True

import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import logging

# Set up logging for debugging
# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

def send_email_report(email_address, pdf_buffer, child_name):
    """Send PDF report via email using Gmail SMTP"""
    try:
        # Gmail SMTP configuration
        HOST = "smtp.gmail.com"
        PORT = 465
        FROM_EMAIL = "pschaudhari1712@gmail.com"  # Your Gmail address
        PASSWORD = "wneltvxtdnvhyhid"  # Your Gmail App Password
        TO_EMAIL = email_address

        # Log the email details for debugging
        # logger.debug(f"Sending email from {FROM_EMAIL} to {TO_EMAIL} for {child_name}")

        # Create email message
        message = MIMEMultipart("alternative")
        message['Subject'] = f"Happiness Report for {child_name}"
        message['From'] = FROM_EMAIL
        message['To'] = TO_EMAIL

        # Email body (HTML)
        html = f"""
        <html>
        <body>
            <p>Hello,</p>
            <p>Attached is the happiness and mental wellness report for {child_name}.</p>
            <p>This report provides insights into how {child_name} is feeling and experiencing emotions.</p>
            <p>Thank you for your commitment to your child's wellbeing.</p>
        </body>
        </html>
        """
        html_part = MIMEText(html, 'html')
        message.attach(html_part)

        # Attach PDF
        pdf_attachment = MIMEApplication(pdf_buffer.read(), _subtype="pdf")
        pdf_buffer.seek(0)  # Reset buffer position
        pdf_attachment.add_header('Content-Disposition', 'attachment', filename='Happiness_Report.pdf')
        message.attach(pdf_attachment)

        # Log the full message for verification
        # logger.debug(f"Email content: {message.as_string()}")

        # Set up SMTP connection with SSL
        smtp = smtplib.SMTP_SSL(HOST, PORT)
        smtp.login(FROM_EMAIL, PASSWORD)
        smtp.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())
        smtp.quit()

        return True, "Email sent successfully!"
    except Exception as e:
        # logger.error(f"Email sending failed: {str(e)}")
        return False, f"Failed to send email: {str(e)}"

# Streamlit UI
if 'report_generated' in st.session_state and st.session_state.report_generated:
    st.subheader("Send Report via Email")
    with st.form(key="email_form"):
        email_address = st.text_input("Enter recipient email address")
        child_name = st.text_input("Enter child's name")
        submit_button = st.form_submit_button(label="Send Report")
        
        if submit_button:
            if email_address and child_name:
                success, message = send_email_report(
                    email_address, 
                    st.session_state.pdf_buffer, 
                    child_name
                )
                if success:
                    st.success(message)
                else:
                    st.error(f"Failed to send email: {message}")
            else:
                st.warning("Please provide both an email address and child's name.")
