import streamlit as st

# Set up page configuration
st.set_page_config(page_title="About Us - Child Mental Health", layout="wide", page_icon="❤️")

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* General Page Styling */
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f9f9f9;
            color: #333;
        }

        /* Header Styling */
        .header-container {
            text-align: center;
            padding: 40px 0;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            border-radius: 15px;
            box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
            margin-bottom: 40px;
        }

        .header-title {
            font-size: 48px;
            font-weight: bold;
            color: #fff;
            margin-bottom: 10px;
        }

        .header-subtitle {
            font-size: 24px;
            color: #fff;
            opacity: 0.9;
        }

        /* Mission, Vision, and Values Section */
        .section {
            padding: 40px 20px;
            margin: 20px 0;
            background-color: #fff;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .section:hover {
            transform: translateY(-5px);
            box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
        }

        .section-title {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #444;
            text-align: center;
        }

        .section-content {
            font-size: 18px;
            color: #666;
            line-height: 1.8;
            text-align: center;
        }

        /* Services Section */
        .services-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            gap: 20px;
        }

        .service-card {
            background-color: #ffffff;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            padding: 30px;
            text-align: center;
            width: 30%;
            min-width: 250px;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .service-card:hover {
            transform: translateY(-10px);
            box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
        }

        .service-icon {
            font-size: 60px;
            color: #2575fc;
            margin-bottom: 20px;
        }

        .service-title {
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        }

        .service-description {
            font-size: 16px;
            color: #555;
        }

        /* Team Section */
        .team-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            gap: 20px;
        }

        .team-member {
            text-align: center;
            width: 30%;
            min-width: 250px;
            background-color: #fff;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
            padding: 20px;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .team-member:hover {
            transform: translateY(-10px);
            box-shadow: 0px 8px 16px rgba(0, 0, 0, 0.2);
        }

        .team-photo {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            object-fit: cover;
            margin-bottom: 15px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }

        .team-name {
            font-size: 20px;
            font-weight: bold;
            color: #333;
            margin-bottom: 5px;
        }

        .team-role {
            font-size: 16px;
            color: #555;
            font-style: italic;
        }

        /* Footer Section */
        .footer {
            margin-top: 40px;
            padding: 20px;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            text-align: center;
            font-size: 16px;
            color: #fff;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    """
    <div class="header-container">
        <div class="header-title">About Us</div>
        <div class="header-subtitle">
            Dedicated to improving children's mental health and providing support to families.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Mission, Vision, and Values Section
st.markdown(
    """
    <div class="section">
        <div class="section-title">Our Mission</div>
        <div class="section-content">
            At the core of our mission is the desire to promote mental well-being among children.  
            We strive to provide families with the tools, resources, and support they need to foster resilience,  
            happiness, and health. Together, we envision a world where mental health challenges are no longer  
            a barrier to a child’s growth and potential.
        </div>
    </div>
    <div class="section">
        <div class="section-title">Our Vision</div>
        <div class="section-content">
            We aspire to create a world where every child feels supported, understood, and empowered to  
            achieve their full potential. Our vision includes eliminating barriers to mental health support,  
            building compassionate communities, and fostering environments where every child can thrive  
            mentally, emotionally, and socially.
        </div>
    </div>
    <div class="section">
        <div class="section-title">Our Core Values</div>
        <div class="section-content">
            Our work is driven by the belief that children’s mental health shapes the future of our society.  
            Every smile, every challenge overcome, and every child supported fuels our passion to do more.  
            By prioritizing children’s mental well-being, we aim to build a generation that is resilient,  
            emotionally intelligent, and prepared to tackle life’s challenges.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Services Section
st.markdown(
    """
    <div class="section">
        <div class="section-title">Our Work</div>
        <div class="services-container">
            <div class="service-card">
                <div class="service-icon">🧠</div>
                <div class="service-title">Chatbot</div>
                <div class="service-description">
                    To solve Parent and Child queries.
                </div>
            </div>
            <div class="service-card">
                <div class="service-icon">📚</div>
                <div class="service-title">Personalized Feedback</div>
                <div class="service-description">
                    To  monitor Mental Health.
                </div>
            </div>
            <div class="service-card">
                <div class="service-icon">🤝</div>
                <div class="service-title">Comparative Study</div>
                <div class="service-description">
                    To compare with other age groups.
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Team Section
st.markdown(
    """
    <div class="section">
        <div class="section-title">Meet Our Team</div>
        <div class="team-container">
            <div class="team-member">
                <div class="team-name">Aryan Manghi</div>
                <div class="team-role">STUDENT</div>
            </div>
            <div class="team-member">
                <div class="team-name">Prasad Chaudhari</div>
                <div class="team-role">STUDENT</div>
            </div>
            <div class="team-member">
                <div class="team-name">Devyaansh Razdan</div>
                <div class="team-role">STUDENT</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Footer Section
st.markdown(
    """
    <div class="footer">
        &copy; 2025 Child Mental Health, Inc. All Rights Reserved.
    </div>
    """,
    unsafe_allow_html=True,
)
