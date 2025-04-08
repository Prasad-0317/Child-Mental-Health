import streamlit as st

# Set up page configuration
st.set_page_config(page_title="Our Motivation - Child Mental Health", layout="wide", page_icon="💡")

# Custom CSS for styling with animations and effects
st.markdown(
    """
    <style>
        /* General Page Styling */
        body {
            font-family: 'Poppins', sans-serif;
            background-color: #f9f9f9;
            color: #333;
        }

        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }

        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }

        @keyframes gradientAnimation {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Header Section */
        .header-container {
            text-align: center;
            padding: 80px 20px;
            background: linear-gradient(-45deg, #6a11cb, #2575fc, #00bfff, #6a11cb);
            background-size: 400% 400%;
            animation: gradientAnimation 15s ease infinite;
            border-radius: 15px;
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
        }

        .header-container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://www.transparenttextures.com/patterns/cubes.png');
            opacity: 0.1;
        }

        .header-title {
            font-size: 52px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 15px;
            animation: fadeIn 1s ease-out;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
        }

        .header-subtitle {
            font-size: 26px;
            color: #fff;
            opacity: 0.95;
            animation: fadeIn 1.2s ease-out;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
            text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
        }

        /* Section Styling */
        .section {
            padding: 50px 30px;
            margin: 30px 0;
            background-color: #fff;
            border-radius: 20px;
            box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.08);
            transition: transform 0.5s ease, box-shadow 0.5s ease;
            animation: fadeIn 0.8s ease-out;
            position: relative;
        }

        .section:hover {
            transform: translateY(-10px);
            box-shadow: 0px 15px 30px rgba(0, 0, 0, 0.15);
        }

        .st-emotion-cache-1104ytp a {
            color: rgb(215 223 231);
            /* text-decoration: underline; */
        }

        .section-title {
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 30px;
            color: #333;
            text-align: center;
            position: relative;
            padding-bottom: 15px;
        }

        .section-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 80px;
            height: 4px;
            background: linear-gradient(to right, #6a11cb, #2575fc);
            border-radius: 2px;
        }

        .section-content {
            font-size: 18px;
            color: #555;
            line-height: 1.9;
            text-align: center;
            max-width: 900px;
            margin: 0 auto;
        }

        /* Motivation Cards */
        .motivation-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            gap: 30px;
            margin-top: 40px;
            perspective: 1000px;
        }

        .motivation-card {
            background-color: #ffffff;
            border-radius: 20px;
            box-shadow: 0px 10px 20px rgba(0, 0, 0, 0.05);
            padding: 40px 30px;
            text-align: center;
            width: 30%;
            min-width: 280px;
            transition: all 0.5s ease;
            transform-style: preserve-3d;
            position: relative;
            overflow: hidden;
        }

        .motivation-card:hover {
            transform: translateY(-15px) rotateY(10deg);
            box-shadow: 0px 20px 40px rgba(0, 0, 0, 0.12);
        }

        .motivation-card::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(45deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.8) 50%, rgba(255,255,255,0) 100%);
            transform: rotate(45deg);
            transition: all 0.8s ease;
            z-index: 1;
        }

        .motivation-card:hover::before {
            animation: shine 1.5s ease;
        }

        @keyframes shine {
            0% { transform: translateX(-100%) rotate(45deg); }
            100% { transform: translateX(100%) rotate(45deg); }
        }

        .motivation-icon-container {
            margin-bottom: 25px;
            position: relative;
            z-index: 2;
        }

        .motivation-icon {
            font-size: 70px;
            width: 100px;
            height: 100px;
            line-height: 100px;
            margin: 0 auto;
            color: #fff;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            border-radius: 50%;
            box-shadow: 0px 10px 20px rgba(37, 117, 252, 0.4);
            position: relative;
            animation: float 3s ease-in-out infinite;
        }

        .motivation-title {
            font-size: 26px;
            font-weight: 600;
            color: #333;
            margin-bottom: 15px;
            position: relative;
            z-index: 2;
        }

        .motivation-description {
            font-size: 17px;
            color: #666;
            line-height: 1.7;
            position: relative;
            z-index: 2;
        }

        /* Footer Section */
        .footer {
            margin-top: 60px;
            padding: 30px;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            text-align: center;
            font-size: 16px;
            color: #fff;
            border-radius: 15px;
            box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.15);
            position: relative;
            overflow: hidden;
        }

        .footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: url('https://www.transparenttextures.com/patterns/cubes.png');
            opacity: 0.1;
        }

        /* Particle Effects */
        .particles {
            position: absolute;
            width: 100%;
            height: 100%;
            top: 0;
            left: 0;
            z-index: 0;
        }

        .particle {
            position: absolute;
            border-radius: 50%;
            opacity: 0.3;
            animation-name: float-particle;
            animation-timing-function: linear;
            animation-iteration-count: infinite;
        }

        @keyframes float-particle {
            0% { transform: translateY(0); opacity: 0; }
            10% { opacity: 0.3; }
            90% { opacity: 0.3; }
            100% { transform: translateY(-500px); opacity: 0; }
        }

        /* Scroll Indicator */
        .scroll-indicator {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 50px;
            height: 50px;
            background-color: #2575fc;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-size: 24px;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            cursor: pointer;
            z-index: 1000;
            animation: pulse 2s infinite;
            transition: all 0.3s ease;
        }

        .scroll-indicator:hover {
            transform: scale(1.1);
            background-color: #6a11cb;
        }

        /* Button Styling */
        .cta-button {
            display: inline-block;
            padding: 15px 30px;
            margin-top: 30px;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            border-radius: 50px;
            font-size: 18px;
            font-weight: 600;
            text-decoration: none;
            box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        .cta-button:hover {
            transform: translateY(-5px);
            box-shadow: 0px 15px 20px rgba(0, 0, 0, 0.2);
        }

        .cta-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(to right, rgba(255,255,255,0.1), rgba(255,255,255,0.5), rgba(255,255,255,0.1));
            transform: translateX(-100%);
            transition: all 0.6s ease;
        }

        .cta-button:hover::before {
            transform: translateX(100%);
        }

        /* Responsive Adjustments */
        @media (max-width: 768px) {
            .header-title {
                font-size: 42px;
            }
            .header-subtitle {
                font-size: 22px;
            }
            .section-title {
                font-size: 30px;
            }
            .motivation-card {
                width: 80%;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add JavaScript for animations and interactivity
st.markdown(
    """
    <script>
        // This script will be executed when the page loads
        document.addEventListener('DOMContentLoaded', function() {
            // Create particles
            const particlesContainer = document.querySelector('.header-container');
            for (let i = 0; i < 50; i++) {
                const particle = document.createElement('div');
                particle.classList.add('particle');
                particle.style.width = Math.random() * 10 + 'px';
                particle.style.height = particle.style.width;
                particle.style.left = Math.random() * 100 + '%';
                particle.style.top = Math.random() * 100 + '%';
                particle.style.backgroundColor = 'rgba(255, 255, 255, ' + (Math.random() * 0.3 + 0.1) + ')';
                particle.style.animationDuration = Math.random() * 15 + 10 + 's';
                particlesContainer.appendChild(particle);
            }
            
            // Scroll indicator
            const scrollIndicator = document.createElement('div');
            scrollIndicator.classList.add('scroll-indicator');
            scrollIndicator.innerHTML = '↑';
            scrollIndicator.addEventListener('click', function() {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            });
            document.body.appendChild(scrollIndicator);
            
            // Show/hide scroll indicator based on scroll position
            window.addEventListener('scroll', function() {
                if (window.scrollY > 300) {
                    scrollIndicator.style.opacity = '1';
                } else {
                    scrollIndicator.style.opacity = '0';
                }
            });
            
            // Animate sections on scroll
            const sections = document.querySelectorAll('.section');
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }
                });
            }, { threshold: 0.1 });
            
            sections.forEach(section => {
                section.style.opacity = '0';
                section.style.transform = 'translateY(50px)';
                section.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
                observer.observe(section);
            });
        });
    </script>
    """,
    unsafe_allow_html=True,
)

# Create a div for particles
particles_div = """
<div class="particles"></div>
"""

# Header Section with Particles
# Header Section 
st.markdown(
    """
    <div class="header-container">
        <div class="header-title">Our Motivation</div>
        <div class="header-subtitle">
            Driven by a deep commitment to improving children's mental health and empowering families worldwide.
        </div>
        <a href="#contact" class="cta-button">Join Our Mission</a>
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
        <div style="text-align: center; margin-top: 30px;">
            <img src="https://www.psychologistehsaas.com/wp-content/uploads/2024/06/Vaishali-SChool.webp" alt="Children's Mental Health" style="max-width: 50%; border-radius: 15px; box-shadow: 0px 10px 20px rgba(0,0,0,0.1);">
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
                <div class="motivation-icon-container">
                    <div class="motivation-icon">❤️</div>
                </div>
                <div class="motivation-title">Compassion</div>
                <div class="motivation-description">
                    We believe every child deserves to feel loved, valued, and supported in their mental health journey.
                    Our approach is rooted in empathy and understanding.
                </div>
            </div>
            <div class="motivation-card">
                <div class="motivation-icon-container">
                    <div class="motivation-icon">🌍</div>
                </div>
                <div class="motivation-title">Global Reach</div>
                <div class="motivation-description">
                    Our mission is to create an inclusive world where mental health resources are accessible to everyone, 
                    regardless of geography, socioeconomic status, or cultural background.
                </div>
            </div>
            <div class="motivation-card">
                <div class="motivation-icon-container">
                    <div class="motivation-icon">💡</div>
                </div>
                <div class="motivation-title">Innovation</div>
                <div class="motivation-description">
                    By leveraging modern technologies and evidence-based practices, we aim to revolutionize mental health care 
                    for children and create solutions that are both effective and engaging.
                </div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Statistics Section
st.markdown(
    """
    <div class="section">
        <div class="section-title">The Impact</div>
        <div class="section-content">
            Understanding the scale of children's mental health challenges drives our commitment to making a difference.
        </div>
        <div style="display: flex; flex-wrap: wrap; justify-content: space-around; margin-top: 40px;">
            <div style="text-align: center; width: 30%; min-width: 200px; margin: 20px; animation: fadeIn 1s ease-out;">
                <div style="font-size: 48px; font-weight: 700; color: #2575fc; margin-bottom: 10px;">1 in 5</div>
                <div style="font-size: 18px; color: #666;">Children experience a mental health condition each year</div>
            </div>
            <div style="text-align: center; width: 30%; min-width: 200px; margin: 20px; animation: fadeIn 1.2s ease-out;">
                <div style="font-size: 48px; font-weight: 700; color: #2575fc; margin-bottom: 10px;">50%</div>
                <div style="font-size: 18px; color: #666;">Of all mental health conditions begin by age 14</div>
            </div>
            <div style="text-align: center; width: 30%; min-width: 200px; margin: 20px; animation: fadeIn 1.4s ease-out;">
                <div style="font-size: 48px; font-weight: 700; color: #2575fc; margin-bottom: 10px;">75%</div>
                <div style="font-size: 18px; color: #666;">Of children with mental health needs don't receive care</div>
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
        <div style="text-align: center; margin-top: 40px;">
            <a href="#join" class="cta-button">How You Can Help</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Testimonial Section
st.markdown(
    """
    <div class="section">
        <div class="section-title">Voices of Change</div>
        <div style="max-width: 800px; margin: 0 auto; padding: 30px; background-color: #f9f9f9; border-radius: 15px; position: relative;">
            <div style="font-size: 64px; color: #2575fc; opacity: 0.2; position: absolute; top: 10px; left: 20px;">"</div>
            <div style="font-size: 18px; color: #555; line-height: 1.8; text-align: center; position: relative; z-index: 2;">
                The work being done here is transformative. By addressing mental health challenges early, 
                we're not just helping individual children – we're changing the trajectory of entire communities 
                and building a more compassionate, understanding world for future generations.
            </div>
            <div style="font-size: 64px; color: #2575fc; opacity: 0.2; position: absolute; bottom: 10px; right: 20px;">"</div>
            <div style="margin-top: 20px; text-align: center;">
                <div style="font-weight: 600; color: #333;">Dr. Krishna Murthy</div>
                <div style="color: #666;">Child Psychologist & Advocate</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Contact Section
st.markdown(
    """
    <div class="section" id="contact">
        <div class="section-title">Join Our Mission</div>
        <div class="section-content">
            Whether you're a mental health professional, a parent, teacher, or simply someone who cares about children's wellbeing, 
            there are many ways to contribute to our mission. Together, we can create meaningful change.
        </div>
        <div style="display: flex; flex-wrap: wrap; justify-content: space-around; margin-top: 40px;">
            <div style="text-align: center; width: 30%; min-width: 250px; margin: 20px; padding: 20px; background-color: #f5f5f5; border-radius: 15px; transition: all 0.3s ease;">
                <div style="font-size: 24px; font-weight: 600; color: #333; margin-bottom: 15px;">Volunteer</div>
                <div style="font-size: 16px; color: #666; line-height: 1.6;">Share your time and skills to support our programs and initiatives.</div>
            </div>
            <div style="text-align: center; width: 30%; min-width: 250px; margin: 20px; padding: 20px; background-color: #f5f5f5; border-radius: 15px; transition: all 0.3s ease;">
                <div style="font-size: 24px; font-weight: 600; color: #333; margin-bottom: 15px;">Donate</div>
                <div style="font-size: 16px; color: #666; line-height: 1.6;">Your financial support helps us expand our reach and impact.</div>
            </div>
            <div style="text-align: center; width: 30%; min-width: 250px; margin: 20px; padding: 20px; background-color: #f5f5f5; border-radius: 15px; transition: all 0.3s ease;">
                <div style="font-size: 24px; font-weight: 600; color: #333; margin-bottom: 15px;">Spread Awareness</div>
                <div style="font-size: 16px; color: #666; line-height: 1.6;">Help us break the stigma around mental health by sharing our message.</div>
            </div>
        </div>
        <div style="text-align: center; margin-top: 40px;">
            <a href="#contact-form" class="cta-button">Contact Us Today</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Footer Section
st.markdown(
    """
    <div class="footer">
        <div style="display: flex; flex-wrap: wrap; justify-content: space-around; max-width: 800px; margin: 0 auto;">
            <div style="margin: 20px; text-align: left;">
                <div style="font-weight: 600; margin-bottom: 10px;">Child Mental Health, Inc.</div>
                <div>123 Wellness Street</div>
                <div>Mumbai, India 400001</div>
            </div>
            <div style="margin: 20px; text-align: left;">
                <div style="font-weight: 600; margin-bottom: 10px;">Contact</div>
                <div>info@childmentalhealth.org</div>
                <div>+91 98765 43210</div>
            </div>
            <div style="margin: 20px; text-align: left;">
                <div style="font-weight: 600; margin-bottom: 10px;">Follow Us</div>
                <div style="display: flex; gap: 15px;">
                    <span style="font-size: 24px;">📱</span>
                    <span style="font-size: 24px;">💻</span>
                    <span style="font-size: 24px;">📸</span>
                </div>
            </div>
        </div>
        <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.2);">
            &copy; 2025 Child Mental Health, Inc. | All Rights Reserved | Mumbai, India
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Add ScrollReveal-like effect with JavaScript
st.markdown(
    """
    <script>
        // Handle scroll animations
        const animateOnScroll = () => {
            const elements = document.querySelectorAll('.section');
            elements.forEach(element => {
                const elementPosition = element.getBoundingClientRect().top;
                const screenPosition = window.innerHeight / 1.3;
                
                if (elementPosition < screenPosition) {
                    element.style.opacity = '1';
                    element.style.transform = 'translateY(0)';
                }
            });
        };
        
        // Set initial state
        document.addEventListener('DOMContentLoaded', () => {
            const elements = document.querySelectorAll('.section');
            elements.forEach(element => {
                element.style.opacity = '0';
                element.style.transform = 'translateY(50px)';
                element.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            });
            
            // Trigger animation on load
            animateOnScroll();
            
            // Trigger animation on scroll
            window.addEventListener('scroll', animateOnScroll);
        });
    </script>
    """,
    unsafe_allow_html=True,
)
