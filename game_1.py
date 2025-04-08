import streamlit as st
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# Configure page settings
st.set_page_config(page_title="Emotional Wellbeing", layout="wide", page_icon="🧩")


# Initialize session state if not already done
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        'name': 'Friend',  # Default name
        'age': 10,         # Default age
        'emotion_scores': {},
        'social_media_hours': 2,
        'social_media_apps': ["YouTube"]
    }

if 'current_page' not in st.session_state:
    st.session_state.current_page = 'emotion_game'

def emotion_matching_game():
    st.title("🧩 Social Media & Emotional Wellbeing")
    st.markdown(f"<h3>Hi {st.session_state.user_data['name']}! Let's explore how social media affects your emotions.</h3>", unsafe_allow_html=True)
    
    # Define emotions based on age group
    if st.session_state.user_data['age'] < 8:
        emotions = {
            "Happy": "Feeling joyful and positive",
            "Sad": "Feeling down or unhappy",
            "Angry": "Feeling frustrated or upset",
            "Scared": "Feeling afraid or worried",
            "Calm": "Feeling peaceful and relaxed"
        }
    else:
        emotions = {
            "Happy": "Feeling joyful and positive",
            "Sad": "Feeling down or unhappy",
            "Angry": "Feeling frustrated or upset",
            "Anxious": "Feeling worried or nervous",
            "Calm": "Feeling peaceful and relaxed",
            "Embarrassed": "Feeling uncomfortable about mistakes",
            "Proud": "Feeling good about accomplishments"
        }
    
    # Initialize or retrieve shuffled emotion order in session state
    if 'shuffled_emotions' not in st.session_state:
        emotion_items = list(emotions.items())
        random.shuffle(emotion_items)
        st.session_state.shuffled_emotions = emotion_items
    else:
        emotion_items = st.session_state.shuffled_emotions
    
    # Store emotion scores
    emotion_scores = st.session_state.user_data.get('emotion_scores', {})
    
    # Add usage time question first
    st.markdown("<div class='card' style='background-color: #f5f5f5; padding: 15px; border-radius: 8px; margin-bottom: 20px;'>", unsafe_allow_html=True)
    st.markdown("<h3>Your Social Media Usage</h3>", unsafe_allow_html=True)
    
    # Get initial usage time or default to 2
    initial_usage = st.session_state.user_data.get('social_media_hours', 2)
    
    # Ask about daily usage time
    social_media_hours = st.slider(
        "How many hours do you spend on social media daily?",
        min_value=0,
        max_value=10,
        value=initial_usage,
        step=1,
        help="Slide to indicate your average daily time on social media platforms"
    )
    
    # Save to session state
    st.session_state.user_data['social_media_hours'] = social_media_hours
    
    # Apps used
    app_options = ["Instagram", "TikTok", "YouTube", "Snapchat", "Facebook", "Twitter/X", "Discord", "WhatsApp", "Other"]
    selected_apps = st.multiselect(
        "Which social media platforms do you use?",
        options=app_options,
        default=st.session_state.user_data.get('social_media_apps', ["YouTube"]),
        help="Select all platforms you regularly use"
    )
    
    # Save to session state
    st.session_state.user_data['social_media_apps'] = selected_apps
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Emotion rating section
    for i, (emotion, description) in enumerate(emotion_items):
        st.markdown(f"<div class='card' style='background-color: #f9f9f9; padding: 15px; border-radius: 8px; margin-bottom: 15px;'><h3>Emotion: {emotion}</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # Use your verified image URLs here
            image_urls = {
                "Happy": "https://img.freepik.com/premium-vector/smiling-chinese-boy-happy-child-avatar-social-networks-vector-illustration_581871-769.jpg?semt=ais_hybrid",
                "Sad": "https://img.freepik.com/premium-vector/sad-boy-sits-floor-has-sad-face_679557-2835.jpg",
                "Angry": "https://thumbs.dreamstime.com/b/boy-angry-face-expression-cartoon-vector-illustrations-isolated-white-little-background-kid-emotion-icons-facial-expressions-141390804.jpg",
                "Scared": "https://thumbs.dreamstime.com/z/little-boy-scared-face-expression-cartoon-vector-illustrations-isolated-white-background-kid-emotion-face-icons-facial-140054489.jpg",
                "Calm": "https://static.vecteezy.com/system/resources/previews/020/314/492/non_2x/cartoon-boy-sitting-and-meditating-free-vector.jpg",
                "Anxious": "https://thumbs.dreamstime.com/b/cute-sad-kid-boy-sitting-alone-scared-vector-164364931.jpg",
                "Embarrassed": "https://thumbs.dreamstime.com/b/embarrassed-cartoon-teenage-boy-drawing-blushing-anime-style-expression-cute-shy-guy-vector-clip-art-illustration-351216295.jpg",
                "Proud": "https://us.123rf.com/450wm/srart/srart2402/srart240200239/226852588-children-portrait-collection-cartoon-vector.jpg?ver=6"
            }
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <img src="{image_urls.get(emotion)}" alt="{emotion} Face" style="width: 150px; height: 150px; object-fit: contain;">
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(f"<p style='font-size: 16px;'>{description}</p>", unsafe_allow_html=True)
            
            # Social media influence question - only ask this single question
            rating_key = f"social_media_{emotion}_{i}"
            
            # Get initial values from existing scores or default to 3
            initial_rating = emotion_scores.get(emotion, {}).get("social_media_rating", 3)
            
            social_media_rating = st.slider(
                f"How often do you feel {emotion} while using social media?",
                min_value=1,
                max_value=5,
                value=initial_rating,
                key=rating_key,
                help=f"1 = Rarely feel {emotion.lower()}, 5 = Frequently feel {emotion.lower()}"
            )
            
            # Update emotion scores
            if emotion not in emotion_scores:
                emotion_scores[emotion] = {}
            
            emotion_scores[emotion]["social_media_rating"] = social_media_rating
            
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Update session state with all emotion scores
    st.session_state.user_data['emotion_scores'] = emotion_scores
    
    # Visualization section
    if emotion_scores:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h2>Your Emotional Response to Social Media</h2>", unsafe_allow_html=True)
        
        # Create dataframe from scores
        emotion_data = []
        for emotion, scores in emotion_scores.items():
            if "social_media_rating" in scores:
                emotion_data.append({
                    "Emotion": emotion,
                    "Rating": scores["social_media_rating"]
                })
        
        df = pd.DataFrame(emotion_data)
        
        # Sort by rating value for better visualization
        df = df.sort_values(by="Rating", ascending=False)
        
        # Create columns for visualization
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Create a bar chart
            fig = px.bar(
                df, 
                x="Emotion", 
                y="Rating",
                color="Rating",
                color_continuous_scale=["blue", "green", "yellow", "orange", "red"],
                title="Your Emotional Response to Social Media",
                labels={"Rating": "Intensity (1-5)"}
            )
            
            fig.update_layout(
                xaxis_title="Emotion",
                yaxis_title="Rating (1-5)",
                yaxis_range=[0, 5.5]
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        # with col2:
        #     # Create a radar chart
        #     categories = df["Emotion"].tolist()
        #     values = df["Rating"].tolist()
            
        #     fig = go.Figure()
            
        #     fig.add_trace(go.Scatterpolar(
        #         r=values,
        #         theta=categories,
        #         fill='toself',
        #         name='Your Emotional Profile'
        #     ))
            
            # fig.update_layout(
            #     polar=dict(
            #         radialaxis=dict(
            #             visible=True,
            #             range=[0, 5]
            #         )
            #     ),
            #     title="Emotional Profile"
            # )
            
            # st.plotly_chart(fig, use_container_width=True)
        
        # Prediction model section
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h2>Mental Health Impact Prediction</h2>", unsafe_allow_html=True)
        
        # Create sample dataset for demonstration (would be replaced with real research data)
        np.random.seed(42)  # For reproducibility
        
        # Create synthetic data based on research correlations
        num_samples = 100
        
        # Simulated data based on social media hours and emotional responses
        X_hours = np.random.normal(loc=3, scale=1.5, size=num_samples)  # Hours distribution
        
        # Create synthetic dataset - positive emotions decrease risk, negative increase
        df_synthetic = pd.DataFrame({
            'social_media_hours': X_hours,
            'happy_rating': np.random.normal(loc=3, scale=1, size=num_samples),
            'sad_rating': np.random.normal(loc=3, scale=1, size=num_samples),
            'angry_rating': np.random.normal(loc=3, scale=1, size=num_samples),
            'anxious_rating': np.random.normal(loc=3, scale=1, size=num_samples),
        })
        
        # Calculate synthetic mental health risk based on research correlations
        df_synthetic['mental_health_risk'] = (
            0.3 * df_synthetic['social_media_hours'] +
            -0.1 * df_synthetic['happy_rating'] +
            0.2 * df_synthetic['sad_rating'] +
            0.15 * df_synthetic['angry_rating'] +
            0.25 * df_synthetic['anxious_rating'] +
            np.random.normal(loc=0, scale=0.5, size=num_samples)  # Random noise
        )
        
        # Scale the risk to 0-100 for easier interpretation
        scaler = StandardScaler()
        df_synthetic['mental_health_risk'] = df_synthetic['mental_health_risk'] - df_synthetic['mental_health_risk'].min()
        df_synthetic['mental_health_risk'] = df_synthetic['mental_health_risk'] / df_synthetic['mental_health_risk'].max() * 100
        
        # Build a simple model
        features = ['social_media_hours', 'happy_rating', 'sad_rating', 'angry_rating', 'anxious_rating']
        X = df_synthetic[features]
        y = df_synthetic['mental_health_risk']
        
        # Train a simple model
        model = LinearRegression()
        model.fit(X, y)
        
        # Prepare user data for prediction
        user_data = {
            'social_media_hours': social_media_hours,
            'happy_rating': emotion_scores.get('Happy', {}).get('social_media_rating', 3),
            'sad_rating': emotion_scores.get('Sad', {}).get('social_media_rating', 3),
            'angry_rating': emotion_scores.get('Angry', {}).get('social_media_rating', 3),
            'anxious_rating': emotion_scores.get('Anxious', {}).get('social_media_rating', 3) 
                           if 'Anxious' in emotion_scores else 
                           emotion_scores.get('Scared', {}).get('social_media_rating', 3)
        }
        
        # Make prediction for user
        user_df = pd.DataFrame([user_data])
        risk_prediction = model.predict(user_df)[0]
        
        # Ensure prediction is within 0-100 range
        risk_prediction = max(0, min(100, risk_prediction))
        
        # Display prediction with gauge chart
        col1, col2 = st.columns([2, 3])
        
        with col1:
            # Create gauge chart
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_prediction,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Estimated Impact Risk"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "darkblue"},
                    'steps' : [
                        {'range': [0, 33], 'color': "lightgreen"},
                        {'range': [33, 66], 'color': "yellow"},
                        {'range': [66, 100], 'color': "salmon"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': risk_prediction
                    }
                }
            ))
            
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("<h3>What This Means</h3>", unsafe_allow_html=True)
            
            # Determine risk category and message
            if risk_prediction < 33:
                risk_category = "Low"
                risk_message = "Your current social media usage appears to have a relatively low negative impact on your mental wellbeing."
                recommendations = [
                    "Continue to be mindful of your social media use",
                    "Maintain healthy boundaries with technology",
                    "Keep track of how different platforms make you feel"
                ]
            elif risk_prediction < 66:
                risk_category = "Moderate"
                risk_message = "Your social media usage may be having some negative effects on your mental wellbeing."
                recommendations = [
                    "Consider setting time limits on your social media use",
                    "Be selective about which content you engage with",
                    "Take regular breaks from social media",
                    "Talk to someone if certain content makes you feel bad"
                ]
            else:
                risk_category = "High"
                risk_message = "Your social media usage patterns and emotional responses suggest a potentially significant impact on your mental wellbeing."
                recommendations = [
                    "Consider significantly reducing time spent on social media",
                    "Use screen time management tools to limit usage",
                    "Talk to a trusted adult about how social media makes you feel",
                    "Consider taking a break from platforms that trigger negative emotions",
                    "Focus on in-person activities and connections"
                ]
            
            st.markdown(f"<p><strong>Risk Level:</strong> {risk_category}</p>", unsafe_allow_html=True)
            st.markdown(f"<p>{risk_message}</p>", unsafe_allow_html=True)
            
            st.markdown("<p><strong>Recommendations:</strong></p>", unsafe_allow_html=True)
            for rec in recommendations:
                st.markdown(f"<p>• {rec}</p>", unsafe_allow_html=True)
            
            st.info("Note: This is an educational simulation based on research trends, not an actual clinical assessment. If you're concerned about your mental health, please talk to a trusted adult, school counselor, or healthcare provider.")
    
    # Educational section about social media impact
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h2>Understanding Social Media's Impact on Mental Health</h2>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["General Impact", "Age-Specific Effects", "Healthy Habits"])
    
    with tab1:
        st.markdown("""
        ### How Social Media Affects Mental Health
        
        Research has shown several ways social media can impact mental wellbeing:
        
        **Positive Effects:**
        - Provides connection with friends and family
        - Offers supportive communities for those with shared interests
        - Can be a creative outlet for self-expression
        - Access to information and educational content
        
        **Negative Effects:**
        - Social comparison and FOMO (Fear of Missing Out) can lead to feelings of inadequacy
        - Cyberbullying and negative interactions can cause distress
        - Sleep disruption from nighttime use affects mood and focus
        - "Filter bubbles" can reinforce negative thinking patterns
        - Addictive design features can lead to unhealthy usage patterns
        
        **Common emotional responses:**
        - **Anxiety** from social comparison and fear of missing out
        - **Depression** symptoms linked to excessive use and negative interactions
        - **Loneliness** despite being "connected"
        - **Body image issues** from exposure to idealized or filtered images
        """)
        
        # Create a visualization of research findings
        st.subheader("Research Findings on Social Media Use")
        
        # Sample data based on research
        research_data = {
            'Finding': [
                'Increased depression with >5h daily use', 
                'Sleep disruption', 
                'Anxiety symptoms', 
                'Positive effect of limiting use',
                'FOMO experiences'
            ],
            'Percentage': [70, 68, 64, 78, 72]
        }
        
        research_df = pd.DataFrame(research_data)
        
        # Create horizontal bar chart
        fig = px.bar(
            research_df,
            x='Percentage',
            y='Finding',
            orientation='h',
            color='Percentage',
            color_continuous_scale='Bluered_r',
            title='Percentage of Adolescents Affected by Social Media (Research Simulation)',
        )
        
        fig.update_layout(
            xaxis_title="Percentage of Adolescents (%)",
            yaxis_title="Research Finding",
            xaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig, use_container_width=True)
            
    with tab2:
        st.markdown("""
        ### Age-Specific Effects
        
        **Children (8-12 years):**
        - Developing brains are more susceptible to addictive patterns
        - May have difficulty distinguishing between reality and curated content
        - More vulnerable to cyberbullying effects
        - Limited ability to self-regulate usage
        
        **Teenagers (13-17 years):**
        - Identity development heavily influenced by social validation
        - Peer approval on social media can impact self-esteem
        - Social comparisons particularly impactful during this period
        - More susceptible to body image issues from filtered content
        
        **Risk Factors That Increase Vulnerability:**
        - Pre-existing mental health conditions
        - Limited parental guidance or monitoring
        - History of bullying or social difficulties
        - Use of multiple platforms for many hours daily
        """)
        
        # Create age-specific impact visualization
        impact_data = {
            'Age Group': ['8-10 years', '11-13 years', '14-16 years', '17-18 years'],
            'Identity Impact': [30, 55, 75, 65],
            'Emotional Impact': [45, 60, 70, 55],
            'Social Skills Impact': [50, 65, 55, 40]
        }
        
        impact_df = pd.DataFrame(impact_data)
        
        # Reshape for plotting
        impact_df_long = pd.melt(
            impact_df, 
            id_vars=['Age Group'], 
            value_vars=['Identity Impact', 'Emotional Impact', 'Social Skills Impact'],
            var_name='Impact Type', 
            value_name='Impact Score'
        )
        
        # Create grouped bar chart
        fig = px.bar(
            impact_df_long,
            x='Age Group',
            y='Impact Score',
            color='Impact Type',
            barmode='group',
            title='How Social Media Affects Different Age Groups',
        )
        
        fig.update_layout(
            xaxis_title="Age Group",
            yaxis_title="Impact Score (0-100)",
            yaxis=dict(range=[0, 100])
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    with tab3:
        st.markdown("""
        ### Developing Healthy Social Media Habits
        
        **Time Management:**
        - Set specific time limits for social media use
        - Use built-in screen time tools on devices
        - Create tech-free zones (like bedrooms) and times (like during meals)
        
        **Content Awareness:**
        - Follow accounts that make you feel good, not worse
        - Unfollow or mute accounts that trigger negative feelings
        - Remember that most content is carefully curated and filtered
        
        **Digital Wellbeing:**
        - Turn off non-essential notifications to reduce distractions
        - Take regular breaks - try a "digital detox" day
        - Practice mindfulness about how social media makes you feel
        
        **Social Connection:**
        - Prioritize real-life interactions over digital ones
        - Use social media to enhance, not replace, in-person connections
        - Talk openly with friends and family about social media experiences
        """)
        
        # Create a pie chart showing healthy vs unhealthy time allocation
        st.subheader("Recommended Daily Activities Balance")
        
        labels = ['Sleep', 'School/Learning', 'Physical Activity', 'Family/Friends', 'Creative Hobbies', 'Social Media', 'Other Screen Time']
        values = [9, 6, 2, 3, 1.5, 1, 1.5]
        
        fig = px.pie(
            values=values,
            names=labels,
            title='Recommended 24-Hour Activity Balance',
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.4
        )
        
        fig.update_traces(textposition='inside', textinfo='percent+label')
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Tips for healthy social media use
        st.subheader("Tips for Better Social Media Use")
        
        tips = [
            "Turn off notifications for social media apps",
            "Set a timer when browsing social platforms",
            "Keep devices out of your bedroom at night",
            "Take a full day break each week (Social Media Sabbath)",
            "Be selective about who you follow",
            "Think before you post or comment",
            "Talk to someone if social media makes you feel bad"
        ]
        
        for i, tip in enumerate(tips, 1):
            st.markdown(f"**{i}. {tip}**")
        
    # Navigation buttons
    st.markdown("<hr>", unsafe_allow_html=True)
    if st.button("Next Game ➡️"):
        st.session_state.current_page = 'situations_game'
        st.rerun()

def situations_game():
    st.title("Next activity would go here")
    st.write("This is a placeholder for the next activity")
    
    if st.button("⬅️ Go Back"):
        st.session_state.current_page = 'emotion_game'
        st.rerun()

# Render the current page
if st.session_state.current_page == 'emotion_game':
    emotion_matching_game()
elif st.session_state.current_page == 'situations_game':
    situations_game()

# Main entry point - add a welcome page or form if needed
if __name__ == "__main__":
    # Only need this if we want to provide a starting form
    pass
