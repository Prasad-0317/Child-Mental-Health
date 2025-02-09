import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Our Motivation - Child Mental Health", layout="wide", page_icon="💡")

# Custom CSS for styling
st.markdown(
    """
    <style>
        /* General Page Styling */
        body {
            font-family: 'Arial', sans-serif;
        }

        /* Header Section */
        .header-container {
            text-align: center;
            padding: 40px 20px;
            background-color: #f5f5f5;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }

        .header-title {
            font-size: 36px;
            font-weight: bold;
            color: #333;
        }

        .header-subtitle {
            font-size: 20px;
            color: #555;
            margin-top: 10px;
        }

        /* Section Styling */
        .section {
            padding: 40px 20px;
            margin: 20px 0;
        }

        .section-title {
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 20px;
            color: #444;
        }

        .section-content {
            font-size: 18px;
            color: #666;
            line-height: 1.8;
        }

        /* Motivation Cards */
        .motivation-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            gap: 20px;
        }

        .motivation-card {
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            padding: 20px;
            text-align: center;
            width: 30%;
            min-width: 250px;
            transition: transform 0.3s, box-shadow 0.3s;
        }

        .motivation-card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 6px 12px rgba(0, 0, 0, 0.2);
        }

        .motivation-icon {
            font-size: 50px;
            color: #007BFF;
            margin-bottom: 10px;
        }

        .motivation-title {
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }

        .motivation-description {
            font-size: 16px;
            color: #555;
        }

        /* Footer Section */
        .footer {
            margin-top: 40px;
            padding: 20px;
            background-color: #f5f5f5;
            text-align: center;
            font-size: 14px;
            color: #777;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header Section
st.markdown(
    """
    <div class="header-container">
        <div class="header-title">Our Motivation</div>
        <div class="header-subtitle">
            Driven by a deep commitment to improving children's mental health and empowering families worldwide.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Inspiration Section
st.markdown(
    """
    <div class="section">
        <div class="section-title">Why We Care</div>
        <div class="section-content">
            Mental health issues among children and adolescents have reached alarming levels globally. 
            As future leaders, thinkers, and innovators, children's well-being directly impacts society's future. 
            Our motivation stems from the desire to bridge gaps in mental health care, eliminate stigma, and provide 
            accessible, compassionate support for every child in need.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Motivation Cards Section
st.markdown(
    """
    <div class="section">
        <div class="section-title">What Drives Us</div>
        <div class="motivation-container">
            <div class="motivation-card">
                <div class="motivation-icon">❤️</div>
                <div class="motivation-title">Compassion</div>
                <div class="motivation-description">
                    We believe every child deserves to feel loved, valued, and supported in their mental health journey.
                </div>
            </div>
            <div class="motivation-card">
                <div class="motivation-icon">🌍</div>
                <div class="motivation-title">Global Reach</div>
                <div class="motivation-description">
                    Our mission is to create an inclusive world where mental health resources are accessible to everyone, regardless of geography.
                </div>
            </div>
            <div class="motivation-card">
                <div class="motivation-icon">💡</div>
                <div class="motivation-title">Innovation</div>
                <div class="motivation-description">
                    By leveraging modern technologies and evidence-based practices, we aim to revolutionize mental health care for children.
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Vision for the Future Section
st.markdown(
    """
    <div class="section">
        <div class="section-title">Our Vision for the Future</div>
        <div class="section-content">
            We envision a future where mental health care is normalized and stigma-free. 
            A world where children can openly express their feelings, seek help without fear, 
            and thrive with the support of their communities and families. This dream drives 
            our daily efforts to innovate, collaborate, and make a meaningful difference.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Footer Section
st.markdown(
    """
    <div class="footer">
        &copy; 2025 Child Mental Health, Inc. | All Rights Reserved | Mumbai, India
    </div>
    """,
    unsafe_allow_html=True,
)
