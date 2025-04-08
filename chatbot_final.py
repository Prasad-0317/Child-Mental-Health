import streamlit as st
import speech_recognition as sr

# Set page configuration
st.set_page_config(
    page_title="Mental Health Support Assistant",
    page_icon="🧠",
    layout="centered"
)

# Initialize session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'last_topic' not in st.session_state:
    st.session_state.last_topic = None

# Custom CSS with colorful balloon animation
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #f0f4ff 0%, #e6f0fa 100%);
        position: relative;
        overflow: hidden;
    }
    .main::before {
        content: '';
        position: absolute;
        width: 100%;
        height: 100%;
        background: inherit;
        z-index: 0;
    }
    /* Balloon animation */
    .balloon {
        position: absolute;
        width: 40px;
        height: 60px;
        border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%;
        animation: floatBalloon 8s infinite ease-in-out;
        z-index: 1;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .balloon:nth-child(1) { 
        background: #ff9999; /* Red */
        left: 15%; 
        bottom: -60px; 
        animation-duration: 9s; 
    }
    .balloon:nth-child(2) { 
        background: #99ccff; /* Blue */
        width: 50px; 
        height: 70px; 
        left: 35%; 
        bottom: -70px; 
        animation-duration: 10s; 
        animation-delay: 2s; 
    }
    .balloon:nth-child(3) { 
        background: #ffcc66; /* Yellow */
        left: 55%; 
        bottom: -40px; 
        animation-duration: 7s; 
        animation-delay: 1s; 
    }
    .balloon:nth-child(4) { 
        background: #99ff99; /* Green */
        width: 45px; 
        height: 65px; 
        left: 75%; 
        bottom: -65px; 
        animation-duration: 8s; 
        animation-delay: 3s; 
    }
    .balloon:nth-child(5) { 
        background: #cc99ff; /* Purple */
        width: 35px; 
        height: 55px; 
        left: 90%; 
        bottom: -55px; 
        animation-duration: 6s; 
        animation-delay: 4s; 
    }
    @keyframes floatBalloon {
        0% { 
            transform: translateY(0) translateX(0); 
            opacity: 1; 
        }
        50% { 
            transform: translateY(-50vh) translateX(20px); 
            opacity: 0.7; 
        }
        100% { 
            transform: translateY(-100vh) translateX(-10px); 
            opacity: 0; 
        }
    }
    .chat-message { 
        padding: 1rem; 
        border-radius: 0.5rem; 
        margin-bottom: 1rem; 
        display: flex; 
        position: relative; 
        z-index: 2; 
        background: rgba(255, 255, 255, 0.9); /* Slight transparency for contrast */
    }
    .chat-message.user { background-color: #2b313e; color: #fff; }
    .chat-message.bot { background-color: #475063; color: #fff; }
    .chat-message .message { flex: 1; }
    .stApp { max-width: 1200px; margin: 0 auto; }
</style>
<div class="balloon"></div>
<div class="balloon"></div>
<div class="balloon"></div>
<div class="balloon"></div>
<div class="balloon"></div>
""", unsafe_allow_html=True)

# Title and introduction
st.title("🧠 Mental Health Support Assistant")
st.markdown("Ask anything about mental health—get quick, personalized guidance!")

# Mental health knowledge base
mental_health_knowledge = {
    "anxiety": {
        "description": "Anxiety is a natural stress response involving excessive worry or fear about future events.",
        "causes": ["High stress", "Trauma", "Genetics", "Caffeine or substance use", "Unresolved conflicts"],
        "symptoms": ["Persistent worry", "Restlessness", "Rapid heartbeat", "Trouble focusing", "Sleep issues"],
        "immediate_coping": ["Deep breathing (4-7-8)", "Grounding (5-4-3-2-1 senses)", "Cold water splash on face", "Short walk"],
        "long_term_management": ["Mindfulness practice", "Regular exercise (30 min/day)", "Therapy (CBT)", "Healthy diet", "Sleep routine"],
        "cautions": ["Avoid overthinking triggers", "Limit overstimulation", "Maintain routine", "Stay hydrated", "Seek early support"],
        "professional_help": ["CBT therapy", "SSRIs or anti-anxiety meds", "Support groups", "Psychiatrist consultation"]
    },
    "depression": {
        "description": "Depression is a mood disorder causing persistent sadness and loss of interest.",
        "causes": ["Loss or trauma", "Chemical imbalances", "Chronic stress", "Isolation", "Family history"],
        "symptoms": ["Ongoing sadness", "Fatigue", "Sleep changes", "Appetite shifts", "Hopelessness"],
        "immediate_coping": ["Talk to someone", "Get sunlight", "Do a small task", "Listen to uplifting music"],
        "long_term_management": ["Set achievable goals", "Exercise regularly", "Therapy (CBT/IP)", "Social connection", "Nutrition focus"],
        "cautions": ["Avoid isolation", "Limit alcohol", "Stick to routines", "Monitor negative thoughts", "Seek help early"],
        "professional_help": ["Psychotherapy (CBT)", "Antidepressants", "TMS or ECT for severe cases", "Counseling"]
    },
    "stress": {
        "description": "Stress is the body’s reaction to pressure, impacting health when chronic.",
        "causes": ["Work demands", "Life changes", "Financial issues", "Lack of rest", "Overcommitment"],
        "symptoms": ["Irritability", "Headaches", "Poor concentration", "Sleep problems", "Muscle tension"],
        "immediate_coping": ["Deep breathing", "Step away briefly", "Drink water", "Stretch or move"],
        "long_term_management": ["Time management", "Regular physical activity", "Mindfulness or yoga", "Set boundaries", "Creative outlets"],
        "cautions": ["Avoid overloading tasks", "Limit screen time", "Ensure rest", "Stay connected", "Address early signs"],
        "professional_help": ["Stress coaching", "MBSR programs", "Biofeedback", "Therapist for burnout"]
    },
    "sleep": {
        "description": "Sleep is crucial for mental health, aiding mood and cognitive function.",
        "causes_of_issues": ["Stress or anxiety", "Screen time", "Caffeine late in day", "Irregular schedule", "Medical conditions"],
        "symptoms_of_issues": ["Difficulty falling asleep", "Frequent waking", "Daytime fatigue", "Irritability"],
        "immediate_coping": ["Relaxing music", "Dark room", "Warm tea (no caffeine)", "Body scan meditation"],
        "long_term_management": ["Consistent sleep schedule", "Bedtime routine", "No screens 1-2 hrs before", "Limit caffeine", "CBT-I"],
        "cautions": ["Avoid late naps", "Limit heavy meals at night", "Reduce evening stress", "Maintain dark room"]
    },
    "crisis": {
        "description": "A mental health crisis involves immediate risk to self or others.",
        "causes": ["Overwhelming despair", "Trauma", "Substance use", "Loss of support"],
        "warning_signs": ["Suicidal thoughts", "Hopelessness", "Reckless behavior", "Extreme mood swings"],
        "immediate_resources": ["Call 988 (Suicide Lifeline)", "Text HOME to 741741", "911 for emergencies", "Trevor Project: 1-866-488-7386"],
        "long_term_management": ["Ongoing therapy", "Build a support network", "Develop coping skills", "Regular mental health check-ins"]
    },
    "self_care": {
        "description": "Self-care involves intentional actions to maintain physical, emotional, and mental well-being.",
        "types": ["Physical (exercise, sleep)", "Emotional (journaling, therapy)", "Social (connecting with others)", "Mental (learning, hobbies)"],
        "immediate_coping": ["Take a 5-min break", "Hydrate", "Step outside", "Positive self-talk"],
        "long_term_management": ["Daily movement", "Balanced diet", "Regular check-ins with self", "Set personal goals"]
    },
    "screen_time": {
        "description": "Screen time refers to time spent on digital devices, impacting mental and physical health.",
        "bad_effects": ["Eye strain", "Poor sleep quality", "Increased stress or anxiety", "Reduced focus", "Social isolation"],
        "reduction_strategies": ["Set screen time limits (e.g., 1-2 hrs/day)", "Use blue light filters", "Take breaks every 30 min", "Replace screen time with hobbies", "No screens 1 hr before bed"],
        "age_recommendations": ["Ages 5-10: 1 hr/day supervised", "Ages 11-15: 2 hrs/day with breaks", "Balance with physical activity and sleep"],
        "immediate_coping": ["Turn off devices for 10 min", "Step outside", "Blink frequently to rest eyes", "Stretch your body"],
        "long_term_management": ["Establish screen-free zones (e.g., bedroom)", "Schedule device-free days", "Promote offline hobbies", "Monitor usage with apps"]
    }
}

# Optimized response function with context
def get_response(query):
    query = query.lower().strip()
    
    if any(kw in query for kw in {"suicide", "kill myself", "end my life", "harm myself", "crisis", "emergency"}):
        info = mental_health_knowledge["crisis"]
        st.session_state.last_topic = "crisis"
        return f"**Immediate Support Needed**:\n\n1. 🚨 {info['description']}\n\n2. 📞 Resources:\n   - {info['immediate_resources'][0]}\n   - {info['immediate_resources'][1]}\n   - {info['immediate_resources'][2]}\n\n3. 💡 Reach out now—your safety matters!"

    topic_keywords = {
        "anxiety": {"anxiety", "anxious", "worry", "panic", "nervous", "fearful"},
        "depression": {"depression", "depressed", "sad", "hopeless", "down", "low"},
        "stress": {"stress", "stressed", "overwhelm", "burnout", "pressure"},
        "sleep": {"sleep", "insomnia", "tired", "rest", "awake", "fatigue"},
        "self_care": {"self-care", "self care", "wellness", "balance", "me time"},
        "screen_time": {"screen time", "phone use", "device", "screen", "digital"}
    }
    
    intent_keywords = {
        "causes": {"why", "cause", "reason", "triggers"},
        "symptoms": {"symptoms", "signs", "feel like", "what happens"},
        "immediate_coping": {"now", "quick", "fast", "immediately", "right away", "what if", "doesn’t work", "can’t"},
        "long_term_management": {"long term", "over time", "manage", "cope", "deal with", "daily", "keep up"},
        "cautions": {"cautions", "prevent", "avoid", "watch out", "worse"},
        "professional_help": {"professional", "therapy", "doctor", "treatment", "help"},
        "types": {"types", "kinds", "options"},
        "bad_effects": {"bad effects", "negative", "harm", "problem"},
        "reduction_strategies": {"reduce", "cut down", "less", "limit"},
        "age_recommendations": {"age", "kids", "children", "teens", "how much"}
    }

    scenarios = {
        "overwhelmed at work": ("stress", "🌟 **Feeling Overwhelmed at Work? Try This**:\n\n1. ⏰ Break tasks into small, manageable chunks.\n\n2. 🌿 Take 5-min breaks to breathe deeply.\n\n3. 🗣️ Discuss workload with a supervisor.\n\n4. 🛌 Prioritize rest to avoid burnout."),
        "can’t sleep because of stress": ("sleep", "🌙 **Can’t Sleep Due to Stress? Here’s Help**:\n\n1. 🧘 Do a 5-min meditation to relax.\n\n2. 📴 No screens 1 hr before bed.\n\n3. ✍️ Write down worries to clear your mind.\n\n4. ☕ Avoid caffeine after midday."),
        "feeling worthless": ("depression", "💙 **Feeling Worthless? You’re Enough**:\n\n1. 🌞 Get 10 min of sunlight or fresh air.\n\n2. 🎯 Complete one small task (e.g., make your bed).\n\n3. 🤝 Call a friend or family member.\n\n4. 🌿 Say: 'My worth isn’t my productivity.'"),
        "panic before exams": ("anxiety", "📚 **Panic Before Exams? Stay Calm**:\n\n1. 🌬️ Use 4-7-8 breathing to steady yourself.\n\n2. ✏️ Study one topic at a time.\n\n3. 🏃 Walk for 5 min to reset.\n\n4. 💬 Affirm: 'I’ve done my best.'"),
        "no energy to do anything": ("depression", "⚡ **No Energy? Start Small**:\n\n1. 💧 Drink water to hydrate.\n\n2. 🌞 Sit by a window or step outside.\n\n3. 🎶 Play a favorite song.\n\n4. 🌱 Set a tiny goal (e.g., stand up for 1 min)."),
        "too much on my mind": ("stress", "🧠 **Too Much on Your Mind? Unload It**:\n\n1. ✍️ Write a quick list of thoughts.\n\n2. 🌿 Breathe deeply for 1 min.\n\n3. ⏰ Focus on one thing for 10 min.\n\n4. 🗣️ Talk it out with someone."),
        "how to start self-care": ("self_care", "🌈 **Starting Self-Care? Easy Steps**:\n\n1. 🚶 Move your body for 5 min.\n\n2. 💧 Sip water mindfully.\n\n3. 📝 Note one thing you’re grateful for.\n\n4. 🌿 Plan 10 min of 'me time' today."),
        "too much screen time": ("screen_time", "📱 **Too Much Screen Time? Here’s Help**:\n\n1. ⏳ Set a timer for 1-2 hrs/day.\n\n2. 🌐 Use blue light filters.\n\n3. 🕒 Take a 5-min break every 30 min.\n\n4. 🎨 Swap screens for a hobby.")
    }

    # Topic detection with context
    topic = None
    for scenario, (scen_topic, response) in scenarios.items():
        if scenario in query:
            topic = scen_topic
            st.session_state.last_topic = topic
            return response
    for t, keywords in topic_keywords.items():
        if any(kw in query for kw in keywords):
            topic = t
            st.session_state.last_topic = topic
            break
    if not topic and st.session_state.last_topic:
        topic = st.session_state.last_topic
    if not topic:
        return "🤔 I’m here to help! Ask about anxiety, depression, stress, sleep, self-care, screen time, or describe your situation (e.g., 'I’m overwhelmed at work'). What’s on your mind?"

    info = mental_health_knowledge[topic]

    # Intent detection with follow-up support
    intent = "long_term_management"  # Default
    for i, keywords in intent_keywords.items():
        if any(kw in query for kw in keywords):
            intent = i
            break

    intent_responses = {
        "causes": (f"🔍 **Causes of {topic.capitalize()}**:", info.get("causes", info.get("causes_of_issues", []))),
        "symptoms": (f"🚩 **Signs of {topic.capitalize()}**:", info.get("symptoms", info.get("symptoms_of_issues", []))),
        "immediate_coping": (f"⏳ **Quick Help for {topic.capitalize()}**:", info.get("immediate_coping", [])),
        "long_term_management": (f"🌱 **Managing {topic.capitalize()} Long-Term**:", info.get("long_term_management", [])),
        "cautions": (f"🛡️ **Cautions for {topic.capitalize()}**:", info.get("cautions", [])),
        "professional_help": (f"🩺 **Professional Help for {topic.capitalize()}**:", info.get("professional_help", [])),
        "types": (f"🌟 **Types of Self-Care**:", info.get("types", []) if topic == "self_care" else []),
        "bad_effects": (f"⚠️ **Bad Effects of Screen Time**:", info.get("bad_effects", []) if topic == "screen_time" else []),
        "reduction_strategies": (f"📴 **How to Reduce Screen Time**:", info.get("reduction_strategies", []) if topic == "screen_time" else []),
        "age_recommendations": (f"⏰ **Acceptable Screen Time (Ages 5-15)**:", info.get("age_recommendations", []) if topic == "screen_time" else [])
    }

    title, items = intent_responses.get(intent, intent_responses["long_term_management"])
    if not items:
        return f"{title}\n\n1. No specific guidance available for this intent."
    return f"{title}\n\n" + "\n\n".join(f"{i+1}. {item}" for i, item in enumerate(items))

# Audio recording function
def record_audio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening... Speak your question")
        audio = r.listen(source)
        try:
            return r.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn’t understand the audio."
        except sr.RequestError:
            return "Network error—please try typing instead."

# Display conversation history
st.write("### Conversation")
for message in st.session_state.conversation_history:
    role_class = "user" if message["role"] == "user" else "bot"
    emoji = "💬" if message["role"] == "user" else "🧠"
    st.markdown(f"""<div class="chat-message {role_class}"><div class="message">{emoji} {message['content']}</div></div>""", unsafe_allow_html=True)

# Input section
audio_col, text_col = st.columns([1, 3])

with audio_col:
    if st.button("🎤 Speak"):
        user_query = record_audio()
        if user_query and not user_query.startswith("Sorry") and not user_query.startswith("Network"):
            st.session_state.conversation_history.append({"role": "user", "content": user_query})
            response = get_response(user_query)
            st.session_state.conversation_history.append({"role": "bot", "content": response})

with text_col:
    with st.form(key="text_form", clear_on_submit=True):
        user_query = st.text_input("Type your question here:", placeholder="Ask me anything...")
        submit_button = st.form_submit_button(label="Send")
        if submit_button and user_query:
            st.session_state.conversation_history.append({"role": "user", "content": user_query})
            response = get_response(user_query)
            st.session_state.conversation_history.append({"role": "bot", "content": response})

# Clear conversation
if st.session_state.conversation_history and st.button("Clear Conversation"):
    st.session_state.conversation_history = []
    st.session_state.last_topic = None
    st.rerun()

# Resources
with st.expander("Additional Resources"):
    st.markdown("""
    - **Crisis Lines (Global)**: 988 (Suicide Lifeline, US) | Text HOME to 741741 (Crisis Text Line, US)
    - **India-Specific Helplines**:
      - **Vandrevala Foundation Helpline**: Call 9999 666 555 (24/7 mental health support across India)
      - **Sneha India**: Call 044-24640050 (Chennai-based, 24/7 suicide prevention helpline) or email help@snehaindia.org
      - **AASRA**: Call 9820466726 (Mumbai-based, 24/7 suicide prevention and emotional support)
      - **iCall (TISS)**: Call 9152987821 (Mon-Sat, 8 AM - 10 PM, psychosocial support by Tata Institute of Social Sciences)
    - **Organizations (Global)**: [NAMI](https://www.nami.org) | [Mental Health America](https://www.mhanational.org)
    - **India-Specific Organizations**:
      - **Sangath**: [www.sangath.in](https://www.sangath.in) - Offers community-based mental health programs and resources for children and families
      - **The Live Love Laugh Foundation**: [www.thelivelovelaughfoundation.org](https://www.thelivelovelaughfoundation.org) - Mental health awareness and support, including resources for parents
      - **Mpower**: [www.mpowerminds.com](https://www.mpowerminds.com) - Provides mental health services and helplines across India
      - **White Swan Foundation**: [www.whiteswanfoundation.org](https://www.whiteswanfoundation.org) - Free online resources and articles on child and adolescent mental health
    - **Self-Help**: [Mindfulness Resources](https://www.mindful.org) | [NIMHANS Well-being Resources](https://www.nimhans.ac.in/departments/nimhans-centre-for-well-being) - Tools and tips from India’s National Institute of Mental Health and Neurosciences
    """)

# Disclaimer
# st.markdown("---")
# st.markdown("**Disclaimer**: This chatbot offers general info, not professional advice. For emergencies, call 988 or 911.")
