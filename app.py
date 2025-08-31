import streamlit as st
import random
import time
from datetime import datetime
import base64
from io import BytesIO
from PIL import Image
import json
import os

# Configure page
st.set_page_config(
    page_title="CAP - Check, Analyze, Practice",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Function to encode image to base64 for HTML embedding
def get_base64_of_bin_file(png_file):
    """Convert image to base64 string"""
    try:
        with open(png_file, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except FileNotFoundError:
        return None

# Custom CSS for better styling with accessibility features
st.markdown("""
<style>
    /* Main styling */
    .main {
        background-color: #f8f9fa;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(90deg, #2c5cc7 0%, #3b8fd9 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    
    /* Tab styling for better accessibility */
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 70px;
        white-space: pre-wrap;
        background-color: #e9ecef;
        border-radius: 8px 8px 0px 0px;
        padding: 15px 20px;
        font-size: 20px;
        font-weight: bold;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2c5cc7;
        color: white;
    }
    
    /* Larger font sizes for accessibility */
    .big-font {
        font-size: 20px !important;
    }
    
    .khmer-font {
        font-family: 'Khmer OS', 'Khmer OS System', sans-serif;
    }
    
    /* Button styling */
    .stButton button {
        font-size: 18px;
        padding: 12px 24px;
    }
    
    /* Card styling */
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #2c5cc7;
        margin: 1rem 0;
    }
    
    .detection-result {
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-size: 18px;
    }
    
    .fake-result {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
    }
    
    .real-result {
        background-color: #e8f5e8;
        border-left: 4px solid #4caf50;
    }
    
    .warning-result {
        background-color: #fff3e0;
        border-left: 4px solid #ff9800;
    }
    
    .score-text {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    
    .khmer-explanation {
        background-color: #f0f5ff;
        padding: 1.2rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-size: 18px;
        border: 1px solid #d0deff;
    }
    
    .header-with-logo {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        margin: 1rem 0;
    }
    
    .sidebar-logo {
        text-align: center;
        padding: 1rem 0;
        border-bottom: 1px solid #eee;
        margin-bottom: 1rem;
    }
    
    .report-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin: 1rem 0;
        font-size: 18px;
    }
    
    .user-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: #2c5cc7;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
        margin-right: 10px;
        font-size: 20px;
    }
    
    .user-info {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .accuracy-badge {
        padding: 6px 12px;
        border-radius: 16px;
        font-size: 16px;
        font-weight: bold;
        margin-left: 10px;
    }
    
    .high-accuracy {
        background-color: #4caf50;
        color: white;
    }
    
    .medium-accuracy {
        background-color: #ff9800;
        color: white;
    }
    
    .low-accuracy {
        background-color: #f44336;
        color: white;
    }
    
    /* Audio button styling */
    .audio-btn {
        background-color: #2c5cc7;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        font-size: 20px;
        cursor: pointer;
        margin-left: 10px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Language toggle */
    .language-toggle {
        display: flex;
        justify-content: center;
        margin: 1rem 0;
    }
    
    .lang-btn {
        padding: 10px 20px;
        margin: 0 5px;
        border: 2px solid #2c5cc7;
        background: white;
        color: #2c5cc7;
        border-radius: 20px;
        font-weight: bold;
        cursor: pointer;
    }
    
    .lang-btn.active {
        background: #2c5cc7;
        color: white;
    }
    
    /* Workshop info */
    .workshop-card {
        background: linear-gradient(135deg, #2c5cc7 0%, #3b8fd9 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Register button styling */
    .register-btn {
        background: linear-gradient(135deg, #4caf50 0%, #2c5cc7 100%);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-weight: bold;
        cursor: pointer;
        margin-top: 10px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'community_reports' not in st.session_state:
    st.session_state.community_reports = [
        {
            'id': 1,
            'type': 'Image',
            'description': 'Fake profile picture with unnatural skin texture',
            'explanation': 'រូបភាពនេះមានសម្បុរាមិនធម្មជាតិ និងភ្នែកមិនស៊ីគ្នា ដែលជាសញ្ញាធម្មតានៃរូបភាព AI',
            'date': '2025-08-20',
            'category': 'Social Media Scam',
            'user': 'Livhoung.H',
            'accuracy': 92,
            'likes': 24,
            'comments': 5
        },
        {
            'id': 2,
            'type': 'News',
            'description': 'False news about government policy',
            'explanation': 'ព័ត៌មានក្លែងក្លាយអំពីគោលនយោបាយរដ្ឋាភិបាល ដែលមិនមានប្រភពជាក់លាក់',
            'date': '2025-08-18',
            'category': 'Political Misinformation',
            'user': 'Pich H.',
            'accuracy': 87,
            'likes': 32,
            'comments': 8
        },
        {
            'id': 3,
            'type': 'Video',
            'description': 'Deepfake video of celebrity endorsement',
            'explanation': 'វីដេអូក្លែងក្លាយដែលប្រើបច្ចេកវិទ្យា deepfake ធ្វើឱ្យតារាចិន្តបង្ហាញពាក្យផ្សាយទំនិញ',
            'date': '2025-08-15',
            'category': 'Commercial Fraud',
            'user': 'Socheata.S',
            'accuracy': 95,
            'likes': 45,
            'comments': 12
        }
    ]

if 'user_score' not in st.session_state:
    st.session_state.user_score = 0

if 'games_played' not in st.session_state:
    st.session_state.games_played = 0

if 'report_to_share' not in st.session_state:
    st.session_state.report_to_share = None

if 'language' not in st.session_state:
    st.session_state.language = 'Khmer'  # Default to Khmer for Cambodian users

if 'registered_workshops' not in st.session_state:
    st.session_state.registered_workshops = []

# Add logo to sidebar if available
with st.sidebar:
    if os.path.exists("logo.png"):
        st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
        st.image("logo.png", width=150)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("### Navigation")
    st.info("Use the tabs above to navigate between different detection tools and resources.")
    
    # Language toggle in sidebar
    st.markdown("### 🌐 Language / ភាសា")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("English", key="en_btn", use_container_width=True):
            st.session_state.language = 'English'
    with col2:
        if st.button("ខ្មែរ", key="kh_btn", use_container_width=True):
            st.session_state.language = 'Khmer'
    
    st.markdown(f"**Selected:** {st.session_state.language}")
    
    # Workshop information
    st.markdown("---")
    st.markdown("### 🎓 Upcoming Workshops")
    
    workshop_info = """
    **Phnom Penh - Sept 15, 2025**
    - How to spot AI scams
    - Using CAP effectively
    - Community reporting
    
    **Siem Reap - Sept 22, 2025**
    - Digital literacy basics
    - Protecting elderly from scams
    """
    
    st.info(workshop_info)
    
    # Register button for workshops
    if st.button("📝 Register for Workshops", key="register_sidebar", use_container_width=True):
        st.session_state.registered_workshops = ["Phnom Penh - Sept 15, 2025", "Siem Reap - Sept 22, 2025"]
        st.success("Registered for all upcoming workshops!")
    
    if os.path.exists("logo.png"):
        st.markdown("---")
        st.markdown("**🔍 CAP**")
        st.markdown("*Check, Analyze, Practice*")
        st.markdown("*ពិនិត្យ វិភាគ អនុវត្ត*")

# Main header with dual language support
st.markdown("""
<div class="main-header">
    <h1>🔍 CAP - Check, Analyze, Practice</h1>
    <p>ពិនិត្យ វិភាគ អនុវត្ត - Protecting Cambodia from AI scams</p>
</div>
""", unsafe_allow_html=True)

# Language-specific welcome message
if st.session_state.language == 'Khmer':
    st.markdown("""
    <div class="big-font">
        <p>ស្វាគមន៍មកកាន់ CAP - ឧបករណ៍កំណត់អត្តសញ្ញាណមាតិកា AI ក្លែងក្លាយសម្រាប់ពលរដ្ឋខ្មែរ</p>
        <p>ជួយការពារខ្លួនអ្នកពីការបោកប្រាស់ដោយ AI និងព័ត៌មានក្លែងក្លាយ</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="big-font">
        <p>Welcome to CAP - AI content detection tool for Cambodian citizens</p>
        <p>Protect yourself from AI scams and misinformation</p>
    </div>
    """, unsafe_allow_html=True)

# Modern tab navigation with larger tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🖼️ Detect Media", 
    "📰 Check News", 
    "🎮 Learn to Spot", 
    "👥 Community", 
    "📚 Learning Hub"
])

# Helper functions
def simulate_image_detection(image_file):
    """Simulate AI detection for images with Khmer explanations"""
    time.sleep(2)  # Simulate processing time
    
    scenarios = [
        {
            'score': random.randint(75, 95),
            'verdict': 'AI Generated (Likely Fake)',
            'khmer_explanation': 'រូបភាពនេះប្រហែលជា AI បង្កើត ដោយសារ:\n• សម្បុរាមិនធម្មជាតិ និងរលោង\n• ភ្នែកមិនស៊ីគ្នា\n• លម្អិតនៅជុំវិញថ្ពាល់មិនច្បាស់',
            'english_explanation': 'This image is likely AI-generated because:\n• Unnatural and smooth skin texture\n• Eyes don\'t match properly\n• Blurry details around the head',
            'technical': 'Detected inconsistencies in facial features and lighting patterns typical of GANs',
            'class': 'fake-result'
        },
        {
            'score': random.randint(15, 40),
            'verdict': 'Real (Human Created)',
            'khmer_explanation': 'រូបភាពនេះគឺពិតប្រាកដ ដោយសារ:\n• សម្បុរាមានលម្អិតធម្មជាតិ\n• ពន្លឺធម្មជាតិ និងស្រមោល\n• លម្អិតតូចៗស្របតាមធម្មជាតិ',
            'english_explanation': 'This image appears authentic because:\n• Natural skin texture with details\n• Natural lighting and shadows\n• Small natural imperfections',
            'technical': 'Natural compression artifacts and lighting consistent with camera capture',
            'class': 'real-result'
        },
        {
            'score': random.randint(45, 65),
            'verdict': 'Uncertain - Needs Review',
            'khmer_explanation': 'មិនអាចកំណត់បានច្បាស់:\n• មានលក្ខណៈលាយបញ្ចូលគ្នា\n• អាចជារូបភាពកែតម្រូវ\n• ត្រូវការការពិនិត្យបន្ថែម',
            'english_explanation': 'Cannot determine with certainty:\n• Mixed characteristics present\n• Possibly heavily edited image\n• Requires additional verification',
            'technical': 'Mixed indicators - possible heavy editing or borderline AI generation',
            'class': 'warning-result'
        }
    ]
    
    return random.choice(scenarios)

def simulate_text_detection(text):
    """Simulate fake news detection with Khmer explanations"""
    time.sleep(1.5)
    
    # Simple keyword-based simulation
    fake_indicators = ['urgent', 'breaking', 'secret', 'hidden truth', 'government cover-up', 'exclusive']
    fake_score = sum(20 for word in fake_indicators if word.lower() in text.lower())
    fake_score += random.randint(0, 40)
    
    scenarios = [
        {
            'score': min(fake_score, 90),
            'verdict': 'Likely Fake News',
            'khmer_explanation': 'ព័ត៌មាននេះអាចជាក្លែងក្លាយ ដោយសារ:\n• ប្រើពាក្យបំផុសអារម្មណ៍\n• គ្មានប្រភពជាក់លាក់\n• ចង់ឱ្យចែករំលែកយ៉ាងលឿន',
            'english_explanation': 'This news is likely fake because:\n• Uses emotional trigger words\n• Lacks specific sources\n• Urges rapid sharing',
            'technical': 'High emotional language, lack of credible sources, urgency indicators',
            'class': 'fake-result'
        },
        {
            'score': random.randint(10, 30),
            'verdict': 'Likely Reliable',
            'khmer_explanation': 'ព័ត៌មាននេះគួរអាចទុកចិត្តបាន:\n• មានប្រភពច្បាស់លាស់\n• ភាសាគ្មានភាពលំអៀង\n• មានលម្អិតពិតប្រាកដ',
            'english_explanation': 'This news appears reliable because:\n• Clear sources are provided\n• Neutral language is used\n• Contains verifiable details',
            'technical': 'Neutral language, credible sources mentioned, factual content structure',
            'class': 'real-result'
        }
    ]
    
    if fake_score > 50:
        return scenarios[0]
    else:
        return scenarios[1]

def generate_spot_challenge():
    """Generate a spot the AI challenge"""
    challenges = [
        {
            'type': 'Image',
            'question': 'Which image is AI generated?',
            'question_khmer': 'តើរូបភាពណាមួយដែល AI បង្កើត?',
            'option_a': '👤 Professional headshot with perfect lighting',
            'option_a_khmer': '👤 រូបថតក្បាលដែលមានពន្លឺល្អឥតខ្ចោះ',
            'option_b': '📷 Casual selfie with natural imperfections',
            'option_b_khmer': '📷 សេលហ្វ៊ីធម្មជាតិដែលមានកំហុសតូចៗ',
            'correct': 'A',
            'explanation': 'AI នឹងបង្កើតរូបភាពដែលល្អឥតខ្ចោះពេក ខណៈដែលរូបថតធម្មតាមានកំហុសតូចៗ',
            'explanation_en': 'AI tends to create images that are too perfect, while real photos have small imperfections'
        },
        {
            'type': 'News',
            'question': 'Which headline is more likely fake?',
            'question_khmer': 'តើចំណងជើងណាមួយដែលអាចជាក្លែងក្លាយ?',
            'option_a': 'Local School Receives Government Funding for New Library',
            'option_a_khmer': 'សាលារៀនមួយទទួលបានថវិកាពីរដ្ឋាភិបាលសម្រាប់បណ្ណាល័យថ្មី',
            'option_b': 'SHOCKING: Secret Government Plan Revealed - Share Before Deleted!',
            'option_b_khmer': 'គួរឱ្យភ្ញាក់ផ្អើល: ផែនការសម្ងាត់របស់រដ្ឋាភិបាលត្រូវបានបង្ហាញ - ចែករំលែកមុនពេលលុប!',
            'correct': 'B',
            'explanation': 'ចំណងជើងដែលប្រើពាក្យ "SHOCKING" និងស្នើសុំឱ្យចែករំលែក តែងតែជាសញ្ញានៃព័ត៌មានក្លែងក្លាយ',
            'explanation_en': 'Headlines using words like "SHOCKING" and urging to share are often signs of fake news'
        },
        {
            'type': 'Video',
            'question': 'Which video description suggests AI generation?',
            'question_khmer': 'តើការពិពណ៌នាវីដេអូណាដែលបង្ហាញថាវាត្រូវបានបង្កើតដោយ AI?',
            'option_a': 'Celebrity cooking tutorial with kitchen mistakes',
            'option_a_khmer': 'ការបង្រៀនធ្វើម្ហូបដោយតារាដែលមានកំហុសក្នុងផ្ទះបាយ',
            'option_b': 'Celebrity perfectly endorsing product with flawless speech',
            'option_b_khmer': 'តារានិយាយផ្សាយទំនិញដ៏ល្អឥតខ្ចោះដោយគ្មានកំហុស',
            'correct': 'B',
            'explanation': 'វីដេអូ AI តែងតែបង្ហាញមនុស្សល្បីនិយាយដ៏ល្អឥតខ្ចោះ ដោយមិនមានកំហុសធម្មជាតិ',
            'explanation_en': 'AI videos often show celebrities speaking perfectly without natural mistakes'
        }
    ]
    return random.choice(challenges)

def get_accuracy_class(accuracy):
    """Get CSS class based on accuracy percentage"""
    if accuracy >= 80:
        return "high-accuracy"
    elif accuracy >= 60:
        return "medium-accuracy"
    else:
        return "low-accuracy"

# Function to simulate audio playback (placeholder)
def play_audio(text):
    """Simulate audio playback (in a real app, this would use TTS)"""
    st.toast("🔊 Playing audio explanation...")

# Function to handle image upload with fake detection
def handle_image_upload():
    """Handle image upload and show fake detection results"""
    if os.path.exists("image.jpeg"):
        # Remove use_container_width parameter for compatibility
        st.image("image.jpeg", caption="Uploaded Image")
        
        # Simulate AI detection
        with st.spinner("Analyzing content... This may take a moment"):
            result = {
                'score': 87,
                'verdict': 'AI Generated (Likely Fake)',
                'khmer_explanation': 'រូបភាពនេះប្រហែលជា AI បង្កើត ដោយសារ:\n• សម្បុរាមិនធម្មជាតិ និងរលោង\n• ភ្នែកមិនស៊ីគ្នា\n• លម្អិតនៅជុំវិញថ្ពាល់មិនច្បាស់',
                'english_explanation': 'This image is likely AI-generated because:\n• Unnatural and smooth skin texture\n• Eyes don\'t match properly\n• Blurry details around the head',
                'technical': 'Detected inconsistencies in facial features and lighting patterns typical of GANs',
                'class': 'fake-result'
            }
        
        # Display results
        st.markdown(f"""
        <div class="detection-result {result['class']}">
            <div class="score-text">{result['verdict']}</div>
            <p><strong>Confidence Score:</strong> {result['score']}%</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Explanation with audio button
        col1, col2 = st.columns([4, 1])
        with col1:
            if st.session_state.language == 'Khmer':
                st.markdown("**🇰🇭 Explanation in Khmer:**")
                st.markdown(f"""
                <div class="khmer-explanation">
                    {result['khmer_explanation']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("**🇺🇸 Explanation in English:**")
                st.markdown(f"""
                <div class="khmer-explanation">
                    {result['english_explanation']}
                </div>
                """, unsafe_allow_html=True)
        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔊", help="Listen to explanation", key="audio_img"):
                if st.session_state.language == 'Khmer':
                    play_audio(result['khmer_explanation'])
                else:
                    play_audio(result['english_explanation'])
        
        # Technical details
        with st.expander("🔬 Technical Details"):
            st.write(result['technical'])
        
        # Store result for potential sharing
        st.session_state.detection_result = result
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📤 Share to Community", key="share_image", use_container_width=True):
                st.session_state.report_to_share = {
                    'type': 'Image',
                    'score': result['score'],
                    'verdict': result['verdict'],
                    'explanation': result['khmer_explanation'] if st.session_state.language == 'Khmer' else result['english_explanation']
                }
                st.success("✅ Ready to share to community! Go to Community Reports tab.")
        with col2:
            if st.button("📥 Save Result", use_container_width=True):
                st.success("✅ Result saved to your reports!")
    else:
        st.warning("Demo image not found. Please add 'image.jpeg' to the same directory as this script.")

# Main content in tabs
with tab1:
    st.header("Media Detection")
    if st.session_state.language == 'Khmer':
        st.markdown("**ផ្ទុកឡើងរូបភាព ឬវីដេអូ ដើម្បីពិនិត្យថាតើវាត្រូវបានបង្កើតដោយ AI**")
    else:
        st.markdown("**Upload an image or video to check if it's AI generated**")
    
    uploaded_file = st.file_uploader(
        "Choose an image or video file" if st.session_state.language == 'English' else "ជ្រើសរើសឯកសាររូបភាព ឬវីដេអូ",
        type=['png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov'],
        help="Supported formats: PNG, JPG, JPEG, GIF, MP4, AVI, MOV"
    )
    
    if uploaded_file is not None:
        # Check if it's the demo image
        if uploaded_file.name == "image.jpeg":
            handle_image_upload()
        else:
            # Display the uploaded file
            if uploaded_file.type.startswith('image'):
                st.image(uploaded_file, caption="Uploaded Image")
            else:
                st.video(uploaded_file)
            
            if st.button("🔍 Analyze Content", type="primary", use_container_width=True):
                with st.spinner("Analyzing content... This may take a moment"):
                    result = simulate_image_detection(uploaded_file)
                
                # Display results
                st.markdown(f"""
                <div class="detection-result {result['class']}">
                    <div class="score-text">{result['verdict']}</div>
                    <p><strong>Confidence Score:</strong> {result['score']}%</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Explanation with audio button
                col1, col2 = st.columns([4, 1])
                with col1:
                    if st.session_state.language == 'Khmer':
                        st.markdown("**🇰🇭 Explanation in Khmer:**")
                        st.markdown(f"""
                        <div class="khmer-explanation">
                            {result['khmer_explanation']}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("**🇺🇸 Explanation in English:**")
                        st.markdown(f"""
                        <div class="khmer-explanation">
                            {result['english_explanation']}
                        </div>
                        """, unsafe_allow_html=True)
                with col2:
                    st.markdown("<br>", unsafe_allow_html=True)
                    if st.button("🔊", help="Listen to explanation", key="audio_img2"):
                        if st.session_state.language == 'Khmer':
                            play_audio(result['khmer_explanation'])
                        else:
                            play_audio(result['english_explanation'])
                
                # Technical details
                with st.expander("🔬 Technical Details"):
                    st.write(result['technical'])
                
                # Store result for potential sharing
                st.session_state.detection_result = result
                
                # Action buttons
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📤 Share to Community", key="share_image2", use_container_width=True):
                        st.session_state.report_to_share = {
                            'type': 'Image',
                            'score': result['score'],
                            'verdict': result['verdict'],
                            'explanation': result['khmer_explanation'] if st.session_state.language == 'Khmer' else result['english_explanation']
                        }
                        st.success("✅ Ready to share to community! Go to Community Reports tab.")
                with col2:
                    if st.button("📥 Save Result", use_container_width=True):
                        st.success("✅ Result saved to your reports!")

with tab2:
    st.header("News Verification")
    if st.session_state.language == 'Khmer':
        st.markdown("**បញ្ចូលខ្លឹមសារព័ត៌មាន ដើម្បីពិនិត្យសញ្ញានៃព័ត៌មានក្លែងក្លាយ**")
    else:
        st.markdown("**Enter text content to check for fake news indicators**")
    
    # Add analyze button before text input    
    text_input = st.text_area(
        "Paste news content or article text here:" if st.session_state.language == 'English' else "បិទភ្ជាប់ខ្លឹមសារព័ត៌មាន ឬអត្ថបទនៅទីនេះ:",
        height=200,
        placeholder="Enter the news article or text you want to analyze..." if st.session_state.language == 'English' else "បញ្ចូលអត្ថបទព័ត៌មានដែលអ្នកចង់វិភាគ..."
    )
    
    # Also add analyze button after text input
    if st.button("🔍 Analyze Text", type="primary", use_container_width=True, key="analyze_btn_second"):
        if not text_input:
            st.warning("Please enter some text to analyze.")
        else:
            with st.spinner("Analyzing text for fake news indicators..."):
                result = simulate_text_detection(text_input)
            
            # Display results
            st.markdown(f"""
            <div class="detection-result {result['class']}">
                <div class="score-text">{result['verdict']}</div>
                <p><strong>Fake News Score:</strong> {result['score']}%</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Explanation with audio button
            col1, col2 = st.columns([4, 1])
            with col1:
                if st.session_state.language == 'Khmer':
                    st.markdown("**🇰🇭 Explanation in Khmer:**")
                    st.markdown(f"""
                    <div class="khmer-explanation">
                        {result['khmer_explanation']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("**🇺🇸 Explanation in English:**")
                    st.markdown(f"""
                    <div class="khmer-explanation">
                        {result['english_explanation']}
                    </div>
                    """, unsafe_allow_html=True)
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🔊", key="audio_news", help="Listen to explanation"):
                    if st.session_state.language == 'Khmer':
                        play_audio(result['khmer_explanation'])
                    else:
                        play_audio(result['english_explanation'])
            
            # Technical details
            with st.expander("🔬 Analysis Details"):
                st.write(result['technical'])
                
            # Store result for potential sharing
            st.session_state.detection_result = result
            
            # Action buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📤 Share to Community", key="share_news", use_container_width=True):
                    st.session_state.report_to_share = {
                        'type': 'News',
                        'score': result['score'],
                        'verdict': result['verdict'],
                        'explanation': result['khmer_explanation'] if st.session_state.language == 'Khmer' else result['english_explanation']
                    }
                    st.success("✅ Ready to share to community! Go to Community Reports tab.")
            with col2:
                if st.button("📥 Save Result", use_container_width=True):
                    st.success("✅ Result saved to your reports!")

with tab3:
    st.header("Learning Games")
    
    if st.session_state.language == 'Khmer':
        st.markdown("**សាកល្បងជំនាញរបស់អ្នកក្នុងការកំណត់អត្តសញ្ញាណមាតិកាដែលបង្កើតដោយ AI!**")
    else:
        st.markdown("**Test your skills at detecting AI-generated content!**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Your Score", st.session_state.user_score)
    with col2:
        st.metric("Games Played", st.session_state.games_played)
    
    if st.button("🎲 Start New Challenge", type="primary", use_container_width=True):
        challenge = generate_spot_challenge()
        st.session_state.current_challenge = challenge
    
    if 'current_challenge' in st.session_state:
        challenge = st.session_state.current_challenge
        
        st.markdown(f"**{challenge['type']} Challenge:**")
        if st.session_state.language == 'Khmer':
            st.markdown(f"### {challenge['question_khmer']}")
        else:
            st.markdown(f"### {challenge['question']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Option A:**")
            if st.session_state.language == 'Khmer':
                st.info(challenge['option_a_khmer'])
            else:
                st.info(challenge['option_a'])
            if st.button("Choose A", key="choice_a", use_container_width=True):
                st.session_state.user_choice = 'A'
        
        with col2:
            st.markdown("**Option B:**")
            if st.session_state.language == 'Khmer':
                st.info(challenge['option_b_khmer'])
            else:
                st.info(challenge['option_b'])
            if st.button("Choose B", key="choice_b", use_container_width=True):
                st.session_state.user_choice = 'B'
        
        if 'user_choice' in st.session_state:
            user_choice = st.session_state.user_choice
            correct_answer = challenge['correct']
            
            st.session_state.games_played += 1
            
            if user_choice == correct_answer:
                st.success("🎉 Correct! Well done!")
                st.session_state.user_score += 1
            else:
                st.error(f"❌ Incorrect. The correct answer was {correct_answer}")
            
            if st.session_state.language == 'Khmer':
                st.markdown("**🇰🇭 Explanation:**")
                st.markdown(f"""
                <div class="khmer-explanation">
                    {challenge['explanation']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("**🇺🇸 Explanation:**")
                st.markdown(f"""
                <div class="khmer-explanation">
                    {challenge['explanation_en']}
                </div>
                """, unsafe_allow_html=True)
            
            # Add audio button for explanation
            if st.button("🔊 Listen to Explanation", key="audio_explanation"):
                if st.session_state.language == 'Khmer':
                    play_audio(challenge['explanation'])
                else:
                    play_audio(challenge['explanation_en'])
            
            # Reset for next challenge
            if st.button("🔄 Next Challenge", use_container_width=True):
                del st.session_state.current_challenge
                del st.session_state.user_choice
                st.rerun()

with tab4:
    st.header("Community Hub")
    
    if st.session_state.language == 'Khmer':
        st.markdown("**មាតិកា AI ដែលរាយការណ៍ដោយសហគមន៍ និងការបោកប្រាស់នៅកម្ពុជា**")
    else:
        st.markdown("**Community-reported AI content and scams in Cambodia**")
    
    # Display existing reports in a feed format
    if st.session_state.language == 'Khmer':
        st.subheader("📊 ការរាយការណ៍សហគមន៍")
    else:
        st.subheader("📊 Community Reports Feed")
    
    for report in reversed(st.session_state.community_reports):
        with st.container():
            st.markdown(f"""
            <div class="report-card">
                <div class="user-info">
                    <div class="user-avatar">{report['user'][0]}</div>
                    <div>
                        <strong>{report['user']}</strong>
                        <span>• {report['date']}</span>
                        <span class="accuracy-badge {get_accuracy_class(report['accuracy'])}">
                            {report['accuracy']}% accurate
                        </span>
                    </div>
                </div>
                <h4>{report['type']}: {report['description']}</h4>
                <p><strong>Category:</strong> {report['category']}</p>
                <div class="khmer-explanation">
                    <strong>🇰🇭 Explanation:</strong> {report['explanation']}
                </div>
                <div style="display: flex; gap: 15px; margin-top: 10px;">
                    <span>👍 {report['likes']}</span>
                    <span>💬 {report['comments']} comments</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add audio button for each report
            if st.button("🔊 Listen to Report", key=f"audio_report_{report['id']}"):
                play_audio(f"{report['description']}. {report['explanation']}")
    
    # Add new report section (initially hidden)
    if st.session_state.language == 'Khmer':
        expander_label = "📝 រាយការណ៍មាតិកា AI ថ្មី"
    else:
        expander_label = "📝 Report New AI Content"
        
    with st.expander(expander_label, expanded=st.session_state.report_to_share is not None):
        # Pre-fill form if there's a report to share from other tabs
        if st.session_state.report_to_share:
            st.info("📤 You have a detection result ready to share with the community!")
            prefilled_description = f"{st.session_state.report_to_share['verdict']} - {st.session_state.report_to_share['type']} detected"
            prefilled_accuracy = st.session_state.report_to_share['score']
            prefilled_explanation = st.session_state.report_to_share['explanation']
        else:
            prefilled_description = ""
            prefilled_accuracy = 0
            prefilled_explanation = ""
        
        with st.form("report_form"):
            if st.session_state.language == 'Khmer':
                content_type = st.selectbox("ប្រភេទមាតិកា", ["Image", "Video", "News", "Social Media Post"])
                description = st.text_area("ការពិពណ៌នា", value=prefilled_description, 
                                          placeholder="ពិពណ៌នាអំពីមាតិកាក្លែងក្លាយ...")
                khmer_explanation = st.text_area("ការពន្យល់ជាភាសាខ្មែរ", value=prefilled_explanation, 
                                                placeholder="ពន្យល់ជាភាសាខ្មែរ...")
                category = st.selectbox("ប្រភេទ", ["Social Media Scam", "Political Misinformation", 
                                                   "Commercial Fraud", "Health Misinformation"])
                
                # Only show accuracy slider if not prefilled from detection
                if st.session_state.report_to_share:
                    accuracy = prefilled_accuracy
                    st.write(f"ការវិភាគយល់ព្រម: {accuracy}%")
                else:
                    accuracy = st.slider("កម្រិតភាពជឿជាក់", 0, 100, prefilled_accuracy)
                
                submit_text = "🚀 ដាក់ស្នើការរាយការណ៍"
            else:
                content_type = st.selectbox("Content Type", ["Image", "Video", "News", "Social Media Post"])
                description = st.text_area("Description", value=prefilled_description, 
                                          placeholder="Describe the fake content...")
                khmer_explanation = st.text_area("Khmer Explanation", value=prefilled_explanation, 
                                                placeholder="Explain in Khmer...")
                category = st.selectbox("Category", ["Social Media Scam", "Political Misinformation", 
                                                   "Commercial Fraud", "Health Misinformation"])
                
                # Only show accuracy slider if not prefilled from detection
                if st.session_state.report_to_share:
                    accuracy = prefilled_accuracy
                    st.write(f"Detection Accuracy: {accuracy}%")
                else:
                    accuracy = st.slider("Accuracy Confidence", 0, 100, prefilled_accuracy)
                
                submit_text = "🚀 Submit Report"
            
            if st.form_submit_button(submit_text, use_container_width=True):
                # Generate a fake user for the demo
                fake_users = ["Livhoung.H", "Pich H.", "Socheata.S", "Dara K.", "Sophea M."]
                
                new_report = {
                    'id': max([r['id'] for r in st.session_state.community_reports], default=0) + 1,
                    'type': content_type,
                    'description': description,
                    'explanation': khmer_explanation,
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'category': category,
                    'user': random.choice(fake_users),
                    'accuracy': accuracy,
                    'likes': random.randint(5, 50),
                    'comments': random.randint(1, 15)
                }
                st.session_state.community_reports.append(new_report)
                
                # Clear the shared report if it was used
                if st.session_state.report_to_share:
                    st.session_state.report_to_share = None
                    
                st.success("✅ Report submitted successfully!")
                st.rerun()

with tab5:
    st.header("Learning Resources")
    
    if st.session_state.language == 'Khmer':
        st.markdown("**ធនធានអប់រំអំពីការកំណត់អត្តសញ្ញាណ AI និងអក្សរសិល្ប៍ឌីជីថល**")
    else:
        st.markdown("**Educational resources about AI detection and digital literacy**")
    
    # Educational sections
    if st.session_state.language == 'Khmer':
        inner_tabs = st.tabs(["🔍 គន្លឹះកំណត់អត្តសញ្ញាណ", "🚨 ការបោកប្រាស់ធម្មតា", "🛡️ ការពារខ្លួន", "❓ សំណួរដែលសួរញឹកញាប់"])
    else:
        inner_tabs = st.tabs(["🔍 Detection Tips", "🚨 Common Scams", "🛡️ Protection Guide", "❓ FAQ"])
    
    with inner_tabs[0]:
        if st.session_state.language == 'Khmer':
            content = """
            ### របៀបកំណត់អត្តសញ្ញាណមាតិកាដែលបង្កើតដោយ AI
            
            **សម្រាប់រូបភាព:**
            - ស្វែងរកវាយនភាពស្បែកដែលមិនធម្មជាតិ
            - ពិនិត្យមើលពន្លឺ និងស្រមោលដែលមិនស្របគ្នា
            - កត់សម្គាល់លក្ខណៈមុខដែលមិនស៊ីមេទ្រី
            - មើលឃើញដៃ ឬម្រាមដៃដែលមានរូបរាងចម្លែក
            """
        else:
            content = """
            ### How to Spot AI-Generated Content
            
            **For Images:**
            - Look for unnatural skin textures
            - Check for inconsistent lighting and shadows
            - Notice asymmetrical facial features
            - Watch for strange hands or fingers
            """
        
        st.markdown(content)
        if st.button("🔊 Listen to Tips", key="audio_tips1"):
            play_audio(content)
    
    with inner_tabs[1]:
        if st.session_state.language == 'Khmer':
            content = """
            ### ការបោកប្រាស់ AI ធម្មតានៅកម្ពុជា
            
            **ការបោកប្រាស់តាមបណ្តាញសង្គម:**
            - ការផ្សាយក្លែងក្លាយពីតារាល្បី
            - ការផ្តល់ជូនល្អពេក
            - សារបន្ទាន់
            """
        else:
            content = """
            ### Common AI Scams in Cambodia
            
            **Social Media Scams:**
            - Fake celebrity endorsements
            - Too-good-to-be-true offers
            - Urgency-based messages
            """
        
        st.markdown(content)
        if st.button("🔊 Listen to Scam Info", key="audio_scams"):
            play_audio(content)
    
    with inner_tabs[2]:
        if st.session_state.language == 'Khmer':
            content = """
            ### របៀបការពារខ្លួនអ្នក
            
            **គន្លឹះទូទៅ:**
            - ត្រួតពិនិត្យប្រភពឱ្យបានច្បាស់
            - កុំចែករំលែកមាតិកាដែលមិនទាន់បានផ្ទៀងផ្ទាត់
            - ប្រើប្រភពច្រើនសម្រាប់ព័ត៌មានសំខាន់
            - សង្ស័យចំពោះសារបន្ទាន់
            """
        else:
            content = """
            ### How to Protect Yourself
            
            **General Tips:**
            - Always verify sources
            - Don't share unverified content
            - Use multiple sources for important news
            - Be skeptical of urgent messages
            """
        
        st.markdown(content)
        if st.button("🔊 Listen to Protection Tips", key="audio_protection"):
            play_audio(content)
    
    with inner_tabs[3]:
        if st.session_state.language == 'Khmer':
            content = """
            ### សំណួរដែលសួរញឹកញាប់
            
            **Q: តើឧបករណ៍កំណត់អត្តសញ្ញាណ AI ត្រឹមត្រូវប៉ុន្មាន?**
            A: ឧបករណ៍របស់យើងផ្តល់នូវការប៉ាន់ស្មានដោយផ្អែកលើលំនាំ AI ធម្មតា។ ត្រូវប្រើវិធីសាស្ត្រផ្ទៀងផ្ទាត់ច្រើនជានិច្ច។
            """
        else:
            content = """
            ### Frequently Asked Questions
            
            **Q: How accurate is the AI detection?**
            A: Our tool provides estimates based on common AI patterns. Always use multiple verification methods.
            """
        
        st.markdown(content)
        if st.button("🔊 Listen to FAQ", key="audio_faq"):
            play_audio(content)
    
    # Workshop information in learning hub
    st.markdown("---")
    st.markdown("""
    <div class="workshop-card">
        <h3>🎓 Join Our Workshops</h3>
        <p>Learn how to spot AI scams and protect your community</p>
        <p><strong>Phnom Penh:</strong> September 15, 2025 - Central Market</p>
        <p><strong>Siem Reap:</strong> September 22, 2025 - Old Market</p>
        <p>Free entry • Khmer language • For all ages</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Add register button in the learning hub as well
    if st.button("📝 Register for Workshops", key="register_learning", use_container_width=True):
        st.session_state.registered_workshops = ["Phnom Penh - Sept 15, 2025", "Siem Reap - Sept 22, 2025"]
        st.success("Registered for all upcoming workshops!")
    
    # Show registration status
    if st.session_state.registered_workshops:
        st.success(f"You are registered for: {', '.join(st.session_state.registered_workshops)}")

# Footer without logo
st.divider()

st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem 0;">
    <p>🔍 CAP - Check, Analyze, Practice - Protecting Cambodia from AI-generated misinformation</p>
    <p>ពិនិត្យ វិភាគ អនុវត្ត - ការពារកម្ពុជាពីព័ត៌មានក្លែងក្លាយដែលបង្កើតដោយ AI</p>
</div>
""", unsafe_allow_html=True)
