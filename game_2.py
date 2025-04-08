import streamlit as st
import random
from PIL import Image
import base64
import pandas as pd
import json
import os
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Social Media Emotion Explorer",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define emotions with descriptions and coping strategies
EMOTIONS = {
    "happy": {
        "description": "A feeling of joy or pleasure",
        "coping_strategies": [
            "🌟 Share your happiness with trusted friends online",
            "🙏 Take a moment to appreciate what made you happy",
            "💌 Use social media to express gratitude for the good things in your life"
        ],
        "emoji": "😊"
    },
    "sad": {
        "description": "A feeling of unhappiness or sorrow",
        "coping_strategies": [
            "🗣️ Talk to a trusted adult about your feelings instead of posting when sad",
            "⏸️ Take a break from social media when feeling down",
            "📸 Remember that what people share online is often only the happy parts of their lives"
        ],
        "emoji": "😢"
    },
    "angry": {
        "description": "A feeling of strong displeasure or annoyance",
        "coping_strategies": [
            "🧘 Take deep breaths and wait before posting when angry",
            "👂 Talk to someone you trust about what made you angry instead of responding online",
            "❓ Remember that messages can be misunderstood online"
        ],
        "emoji": "😠"
    },
    "scared": {
        "description": "A feeling of fear or being frightened",
        "coping_strategies": [
            "🛡️ Talk to a trusted adult about anything online that scares you",
            "🚫 Remember you can block and report things that make you uncomfortable",
            "⏰ Set healthy boundaries for your online time"
        ],
        "emoji": "😨"
    },
    "surprised": {
        "description": "A feeling of being amazed or astonished",
        "coping_strategies": [
            "🤔 Take a moment to think about unexpected content before sharing it",
            "🔍 Verify surprising information before believing or sharing it",
            "❓ Ask a trusted adult about surprising things you see online"
        ],
        "emoji": "😲"
    },
    "disgusted": {
        "description": "A feeling of strong dislike or aversion",
        "coping_strategies": [
            "🚩 Report inappropriate content that disgusts you",
            "🗣️ Talk to a trusted adult about content that bothers you",
            "👀 Remember you can choose what you look at online"
        ],
        "emoji": "🤢"
    }
}

# Sample scenarios for emotion identification - SOCIAL MEDIA FOCUS
SCENARIOS = [
    {"scenario": "Alex notices their friend is spending 8 hours a day on their phone instead of playing outside.", "emotion": "sad"},
    {"scenario": "Sam's parent told them not to use social media, but Sam discovers their friend is using it anyway.", "emotion": "surprised"},
    {"scenario": "Jamie received 50 likes on the artwork they shared online.", "emotion": "happy"},
    {"scenario": "Casey saw a scary video that someone shared in a group chat late at night.", "emotion": "scared"},
    {"scenario": "Jordan's friend posted an embarrassing photo of them without asking permission.", "emotion": "angry"},
    {"scenario": "Taylor found inappropriate content while browsing videos online.", "emotion": "disgusted"},
    {"scenario": "Riley's online friend sent them a kind message when they were having a bad day.", "emotion": "happy"},
    {"scenario": "Morgan saw their friends posting about a party they weren't invited to.", "emotion": "sad"},
    {"scenario": "Pat's parent set a 1-hour daily limit on their game time.", "emotion": "sad"},
    {"scenario": "Quinn received a message from someone they don't know asking for personal information.", "emotion": "scared"},
    {"scenario": "Avery discovered their favorite author replied to their comment online.", "emotion": "surprised"},
    {"scenario": "Bailey saw someone being mean to others in an online game chat.", "emotion": "disgusted"}
]

# Initialize session state variables if they don't exist
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'current_scenario' not in st.session_state:
    st.session_state.current_scenario = random.choice(SCENARIOS)
if 'game_screen' not in st.session_state:
    st.session_state.game_screen = "login"
if 'user_data' not in st.session_state:
    st.session_state.user_data = {"name": "", "age": 0}
if 'history' not in st.session_state:
    st.session_state.history = []
if 'game_round' not in st.session_state:
    st.session_state.game_round = 0
if 'used_scenarios' not in st.session_state:
    st.session_state.used_scenarios = []
if 'game_complete' not in st.session_state:
    st.session_state.game_complete = False
if 'max_rounds' not in st.session_state:
    st.session_state.max_rounds = 5  # Set to 5 questions total

# Function to save user progress
def save_progress():
    if not os.path.exists("data"):
        os.makedirs("data")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    progress_data = {
        "timestamp": timestamp,
        "name": st.session_state.user_data["name"],
        "age": st.session_state.user_data["age"],
        "points": st.session_state.points,
        "rounds_played": st.session_state.game_round,
        "history": st.session_state.history
    }
    
    filename = f"data/progress_{st.session_state.user_data['name']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    
    with open(filename, "w") as f:
        json.dump(progress_data, f)

# Function to reset the game
def reset_game():
    st.session_state.points = 0
    st.session_state.game_round = 0
    st.session_state.history = []
    st.session_state.used_scenarios = []
    st.session_state.game_screen = "login"
    st.session_state.user_data = {"name": "", "age": 0}
    st.session_state.game_complete = False

# Function to get a new scenario
def get_new_scenario():
    available_scenarios = [s for s in SCENARIOS if s not in st.session_state.used_scenarios]
    
    # If we've used all scenarios, reset the used list
    if not available_scenarios:
        st.session_state.used_scenarios = []
        available_scenarios = SCENARIOS
    
    scenario = random.choice(available_scenarios)
    st.session_state.used_scenarios.append(scenario)
    return scenario

# Function to check the answer
def check_answer(selected_emotion):
    correct_emotion = st.session_state.current_scenario["emotion"]
    is_correct = selected_emotion == correct_emotion
    
    if is_correct:
        st.session_state.points += 10
    
    # Record history
    st.session_state.history.append({
        "round": st.session_state.game_round + 1,  # +1 for human-readable round numbers
        "scenario": st.session_state.current_scenario["scenario"],
        "correct_emotion": correct_emotion,
        "selected_emotion": selected_emotion,
        "is_correct": is_correct
    })
    
    st.session_state.game_round += 1
    
    # Check if game is complete
    if st.session_state.game_round >= st.session_state.max_rounds:
        st.session_state.game_complete = True
        st.session_state.game_screen = "summary"
    else:
        # Get new scenario for next round
        st.session_state.current_scenario = get_new_scenario()
        # Show result screen
        st.session_state.game_screen = "result"
    
    return is_correct, correct_emotion

# Custom CSS
st.markdown("""
<style>
    .main-title {
        font-size: 3em;
        font-weight: bold;
        text-align: center;
        color: #4B0082;
        margin-bottom: 20px;
    }
    .sub-title {
        font-size: 1.5em;
        text-align: center;
        color: #8A2BE2;
        margin-bottom: 30px;
    }
    .emotion-card {
        background-color: #f9f9f9;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        text-align: center;
    }
    .emotion-emoji {
        font-size: 3em;
        margin-bottom: 10px;
    }
    .points-display {
        font-size: 1.5em;
        font-weight: bold;
        color: #4B0082;
        text-align: center;
        margin: 20px 0;
    }
    .scenario-text {
        font-size: 1.8em;
        text-align: center;
        margin: 30px 0;
        padding: 20px;
        background-color: #f0f0f0;
        border-radius: 10px;
    }
    .result-text {
        font-size: 2em;
        text-align: center;
        margin: 20px 0;
        font-weight: bold;
    }
    .coping-strategy {
        background-color: #e6f7ff;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 1.1em;
    }
    .input-field {
        margin: 20px 0;
    }
    .summary-item {
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        font-size: 1.1em;
    }
    .correct-answer {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
    }
    .wrong-answer {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
    }
    .round-indicator {
        text-align: center;
        color: #6c757d;
        font-size: 1.2em;
        margin: 15px 0;
    }
    .summary-header {
        text-align: center;
        font-size: 1.5em;
        margin: 20px 0;
        padding: 10px;
        background-color: #e9ecef;
        border-radius: 10px;
    }
    .tip-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 15px;
        border-radius: 12px;
        margin: 15px 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .tip-card:hover {
        transform: translateY(-5px);
    }
    .tip-emoji {
        font-size: 2em;
        margin-right: 10px;
        display: inline-block;
    }
    .tip-text {
        display: inline-block;
        vertical-align: middle;
        font-size: 1.1em;
    }
</style>
""", unsafe_allow_html=True)

# Login Screen
if st.session_state.game_screen == "login":
    st.markdown("<div class='main-title'>Social Media Emotion Explorer</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Learn about emotions and social media!</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.form("login_form"):
            st.markdown("<div class='input-field'>", unsafe_allow_html=True)
            name = st.text_input("What's your name?", key="name_input")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='input-field'>", unsafe_allow_html=True)
            age = st.number_input("How old are you?", min_value=4, max_value=12, value=8, step=1, key="age_input")
            st.markdown("</div>", unsafe_allow_html=True)
            
            submitted = st.form_submit_button("Let's Play!")
            
            if submitted:
                if name.strip():  # Make sure name is not empty
                    st.session_state.user_data = {"name": name, "age": age}
                    st.session_state.game_screen = "game"
                    st.rerun()

# Game Screen
elif st.session_state.game_screen == "game":
    # Header
    st.markdown("<div class='main-title'>Social Media Emotion Explorer</div>", unsafe_allow_html=True)
    
    # Display user info and points
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"<div style='text-align: center;'>Hi, {st.session_state.user_data['name']} (Age: {st.session_state.user_data['age']})</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='points-display'>Points: {st.session_state.points}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='round-indicator'>Question {st.session_state.game_round + 1} of {st.session_state.max_rounds}</div>", unsafe_allow_html=True)
    
    # Display current scenario
    st.markdown(f"<div class='scenario-text'>{st.session_state.current_scenario['scenario']}</div>", unsafe_allow_html=True)
    
    # Display emotion options
    st.markdown("<div style='text-align: center; margin: 20px 0;'>How would someone feel in this situation?</div>", unsafe_allow_html=True)
    
    # Create a 3x2 grid of emotion buttons
    col1, col2, col3 = st.columns(3)
    
    emotions = list(EMOTIONS.keys())
    
    # First row
    with col1:
        st.markdown(f"<div class='emotion-emoji'>{EMOTIONS[emotions[0]]['emoji']}</div>", unsafe_allow_html=True)
        if st.button(emotions[0].capitalize(), key=emotions[0], use_container_width=True):
            is_correct, correct_emotion = check_answer(emotions[0])
    
    with col2:
        st.markdown(f"<div class='emotion-emoji'>{EMOTIONS[emotions[1]]['emoji']}</div>", unsafe_allow_html=True)
        if st.button(emotions[1].capitalize(), key=emotions[1], use_container_width=True):
            is_correct, correct_emotion = check_answer(emotions[1])
    
    with col3:
        st.markdown(f"<div class='emotion-emoji'>{EMOTIONS[emotions[2]]['emoji']}</div>", unsafe_allow_html=True)
        if st.button(emotions[2].capitalize(), key=emotions[2], use_container_width=True):
            is_correct, correct_emotion = check_answer(emotions[2])
    
    # Second row
    with col1:
        st.markdown(f"<div class='emotion-emoji'>{EMOTIONS[emotions[3]]['emoji']}</div>", unsafe_allow_html=True)
        if st.button(emotions[3].capitalize(), key=emotions[3], use_container_width=True):
            is_correct, correct_emotion = check_answer(emotions[3])
    
    with col2:
        st.markdown(f"<div class='emotion-emoji'>{EMOTIONS[emotions[4]]['emoji']}</div>", unsafe_allow_html=True)
        if st.button(emotions[4].capitalize(), key=emotions[4], use_container_width=True):
            is_correct, correct_emotion = check_answer(emotions[4])
    
    with col3:
        st.markdown(f"<div class='emotion-emoji'>{EMOTIONS[emotions[5]]['emoji']}</div>", unsafe_allow_html=True)
        if st.button(emotions[5].capitalize(), key=emotions[5], use_container_width=True):
            is_correct, correct_emotion = check_answer(emotions[5])

# Result Screen
elif st.session_state.game_screen == "result":
    last_result = st.session_state.history[-1]
    is_correct = last_result["is_correct"]
    correct_emotion = last_result["correct_emotion"]
    selected_emotion = last_result["selected_emotion"]
    
    st.markdown("<div class='main-title'>Social Media Emotion Explorer</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(f"<div class='round-indicator'>Question {last_result['round']} of {st.session_state.max_rounds}</div>", unsafe_allow_html=True)
        
        if is_correct:
            st.markdown(f"<div class='result-text' style='color: green;'>Correct! 🎉</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-size: 1.5em;'>You earned 10 points!</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='result-text' style='color: #FF6347;'>Not quite right</div>", unsafe_allow_html=True)
            st.markdown(f"<div style='text-align: center; font-size: 1.5em;'>The feeling was <b>{correct_emotion}</b> {EMOTIONS[correct_emotion]['emoji']}</div>", unsafe_allow_html=True)
        
        st.markdown(f"<div class='points-display'>Total Points: {st.session_state.points}</div>", unsafe_allow_html=True)
        
        # Show emotion information
        st.markdown(f"<h3>About feeling {correct_emotion} {EMOTIONS[correct_emotion]['emoji']}</h3>", unsafe_allow_html=True)
        st.write(EMOTIONS[correct_emotion]['description'])
        
        st.markdown("<h3>Helpful strategies for social media:</h3>", unsafe_allow_html=True)
        for strategy in EMOTIONS[correct_emotion]['coping_strategies']:
            st.markdown(f"<div class='coping-strategy'>{strategy}</div>", unsafe_allow_html=True)
        
        # Navigation button
        if st.button("Continue", use_container_width=True):
            st.session_state.game_screen = "game"
            st.rerun()

# Summary Screen (Game Complete)
elif st.session_state.game_screen == "summary":
    st.markdown("<div class='main-title'>Social Media Emotion Explorer</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>Game Complete!</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Display final score
        st.markdown(f"<div class='points-display'>Final Score: {st.session_state.points} / {st.session_state.max_rounds * 10}</div>", unsafe_allow_html=True)
        
        # Calculate performance
        correct_answers = sum(1 for item in st.session_state.history if item["is_correct"])
        percentage_correct = (correct_answers / st.session_state.max_rounds) * 100
        
        if percentage_correct >= 80:
            message = "Amazing job! You're an emotion expert! 🌟"
        elif percentage_correct >= 60:
            message = "Great work! You understand emotions well! 👍"
        else:
            message = "Good try! Keep learning about emotions! 💪"
        
        st.markdown(f"<div style='text-align: center; font-size: 1.5em; margin: 20px 0;'>{message}</div>", unsafe_allow_html=True)
        
        # Show summary of all questions and answers
        st.markdown("<div class='summary-header'>Your Answers</div>", unsafe_allow_html=True)
        
        for item in st.session_state.history:
            if item["is_correct"]:
                st.markdown(f"<div class='summary-item correct-answer'><b>Question {item['round']}:</b> {item['scenario']}<br><b>Your answer:</b> {item['selected_emotion'].capitalize()} {EMOTIONS[item['selected_emotion']]['emoji']} ✓</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='summary-item wrong-answer'><b>Question {item['round']}:</b> {item['scenario']}<br><b>Your answer:</b> {item['selected_emotion'].capitalize()} {EMOTIONS[item['selected_emotion']]['emoji']} ✗<br><b>Correct answer:</b> {item['correct_emotion'].capitalize()} {EMOTIONS[item['correct_emotion']]['emoji']}</div>", unsafe_allow_html=True)
        
        # Social media tips with emojis and fancy styling
        st.markdown("<div class='summary-header'>✨ Social Media Tips for Kids ✨</div>", unsafe_allow_html=True)
        
        tips = [
            {"emoji": "🔒", "tip": "Never share personal information with strangers online"},
            {"emoji": "⏰", "tip": "Set screen time limits and take regular breaks to play outside"},
            {"emoji": "🧠", "tip": "Not everything you see online is true - think before you believe"},
            {"emoji": "❤️", "tip": "Be kind in your comments - your words can affect others"},
            {"emoji": "🗣️", "tip": "Always talk to a trusted adult if something makes you uncomfortable"},
            {"emoji": "🚫", "tip": "Know how to block and report content or people that upset you"},
            {"emoji": "😊", "tip": "Remember that most people only share their happiest moments online"},
            {"emoji": "👪", "tip": "Spend time with family and friends in real life, not just online"}
        ]
        
        for tip in tips:
            st.markdown(f"""
            <div class='tip-card'>
                <span class='tip-emoji'>{tip['emoji']}</span>
                <span class='tip-text'>{tip['tip']}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Navigation buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Play Again", use_container_width=True):
                save_progress()
                reset_game()
                st.rerun()
        with col2:
            if st.button("Quit Game", use_container_width=True):
                save_progress()
                reset_game()
                st.rerun()

# Add a sidebar for game stats and quit option
with st.sidebar:
    if st.session_state.game_screen != "login":
        st.markdown(f"<div style='text-align: center; font-weight: bold;'>Game Stats</div>", unsafe_allow_html=True)
        st.markdown(f"Player: {st.session_state.user_data['name']}")
        st.markdown(f"Age: {st.session_state.user_data['age']}")
        st.markdown(f"Points: {st.session_state.points}")
        st.markdown(f"Question: {st.session_state.game_round}/{st.session_state.max_rounds}")
        
        if st.button("Quit Game"):
            save_progress()
            reset_game()
            st.rerun()
