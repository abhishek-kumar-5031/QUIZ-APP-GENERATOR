import streamlit as st
import json
import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError
import time

# Load environment variables
load_dotenv()

# Set up GitHub AI client
token = os.getenv("GITHUB_TOKEN")
if not token:
    st.error("⚠️ GitHub Token not found! Please check your .env file.")
    
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

# Cache function to avoid repeated API calls
@st.cache_data
def fetch_questions(text_content, quiz_level):
    RESPONSE_JSON = {
        "mcqs": [
            {
                "mcq": "Sample question 1",
                "options": {"a": "Choice 1", "b": "Choice 2", "c": "Choice 3", "d": "Choice 4"},
                "correct": "a",
            }
        ]
    }

    PROMPT_TEMPLATE = """You are an expert in generating MCQ quizzes. Based on the given text, create a quiz with 3 multiple-choice questions.
    Return only raw JSON without any markdown formatting or code blocks. The response must follow this structure exactly:
    {
        "mcqs": [
            {
                "mcq": "Question text here",
                "options": {
                    "a": "Option A",
                    "b": "Option B",
                    "c": "Option C",
                    "d": "Option D"
                },
                "correct": "a"
            }
        ]
    }
    
    Text to generate questions from: """ + text_content

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {
                    "role": "system",
                    "content": "You are a quiz generator that only responds with raw JSON. Do not include markdown formatting, code blocks, or any other text."
                },
                {
                    "role": "user",
                    "content": PROMPT_TEMPLATE
                }
            ],
            temperature=0.3,
            max_tokens=1000
        )

        extracted_response = response.choices[0].message.content.strip()
        cleaned_response = extracted_response.replace("```json", "").replace("```", "").strip()
        
        try:
            parsed_json = json.loads(cleaned_response)
            mcqs = parsed_json.get("mcqs", [])
            if not mcqs:
                st.warning("No questions were generated. Please try again.")
                return []
            return mcqs
        except json.JSONDecodeError as je:
            st.error("Failed to generate quiz. Please try again.")
            return []
    
    except OpenAIError as e:
        st.error(f"❌ API error: {e}")
        return []

# Advanced styling with glassmorphism and modern UI trends
st.markdown("""
<style>
    /* Modern Color Scheme */
    :root {
        --primary: #6366f1;
        --secondary: #8b5cf6;
        --success: #10b981;
        --error: #ef4444;
        --background: #0f172a;
        --text: #f8fafc;
        --card: rgba(255, 255, 255, 0.1);
    }

    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, var(--background), #1e293b);
        color: var(--text);
    }

    /* Glassmorphism Effect */
    .glass-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    /* Modern Button Styles */
    .custom-button {
        background: linear-gradient(45deg, var(--primary), var(--secondary));
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        color: white;
        font-weight: 600;
        transition: all 0.3s ease;
        transform: translateY(0);
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }

    .custom-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
    }

    /* Progress Bar */
    .progress-container {
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        margin: 1rem 0;
        overflow: hidden;
    }

    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        transition: width 0.3s ease;
    }

    /* Stats Card */
    .stats-card {
        background: var(--card);
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .animate-fade-in {
        animation: fadeIn 0.5s ease forwards;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state with advanced tracking
if 'session_data' not in st.session_state:
    st.session_state.session_data = {
        'quiz_history': [],
        'total_questions_answered': 0,
        'correct_answers': 0,
        'average_time_per_question': 0,
        'difficulty_stats': {'Easy': 0, 'Medium': 0, 'Hard': 0},
        'current_streak': 0,
        'best_streak': 0
    }

def main():
    # Custom title with emoji and gradient
    st.markdown("""
        <h1 style='background: linear-gradient(45deg, #6366f1, #8b5cf6);
                   -webkit-background-clip: text;
                   -webkit-text-fill-color: transparent;
                   font-size: 3rem;
                   text-align: center;
                   margin-bottom: 2rem;'>
            🚀 Future Quiz AI
        </h1>
    """, unsafe_allow_html=True)

    # Sidebar with glass effect
    with st.sidebar:
        # User profile section
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(139, 92, 246, 0.1));
            border-radius: 15px;
            padding: 1rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        '>
            <h2 style='
                background: linear-gradient(45deg, #6366f1, #8b5cf6);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0;
                font-size: 1.5rem;
            '>Abhishek Kumar</h2>
            <p style='
                color: rgba(255, 255, 255, 0.7);
                margin: 0.5rem 0 0 0;
                font-size: 0.9rem;
            '>Quiz Master</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
        st.markdown("### 🎮 Control Center")
        
        # Advanced configuration options
        text_content = st.text_area("📝 Knowledge Input", height=150)
        quiz_level = st.select_slider("🎯 Challenge Level", 
                                    options=["Easy", "Medium", "Hard"],
                                    value="Medium")
        
        # Advanced settings
        with st.expander("⚙️ Advanced Settings"):
            question_count = st.slider("Questions", 3, 10, 5)
            time_limit = st.slider("Time per Question (seconds)", 30, 120, 60)
            enable_hints = st.toggle("Enable AI Hints", True)
        
        if st.button("🎲 Generate Challenge", type="primary"):
            with st.spinner("🤖 Crafting your personalized quiz..."):
                questions = fetch_questions(text_content, quiz_level)
                if questions:
                    st.session_state.questions = questions[:question_count]
                    st.session_state.quiz_generated = True
                    st.session_state.current_question = 0
                    st.session_state.score = 0
                    st.session_state.show_results = False
                    st.session_state.start_time = time.time()
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Stats Display
        if st.session_state.session_data['total_questions_answered'] > 0:
            st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
            st.markdown("### 📊 Performance Analytics")
            
            accuracy = (st.session_state.session_data['correct_answers'] / 
                       st.session_state.session_data['total_questions_answered'] * 100)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Accuracy", f"{accuracy:.1f}%")
                st.metric("Best Streak", st.session_state.session_data['best_streak'])
            with col2:
                st.metric("Questions", st.session_state.session_data['total_questions_answered'])
                st.metric("Avg Time", f"{st.session_state.session_data['average_time_per_question']:.1f}s")
            
            # Difficulty distribution
            st.markdown("#### Difficulty Distribution")
            diff_stats = st.session_state.session_data['difficulty_stats']
            total = sum(diff_stats.values())
            if total > 0:
                for diff, count in diff_stats.items():
                    percentage = (count / total) * 100
                    st.progress(percentage / 100, text=f"{diff}: {percentage:.1f}%")
            st.markdown("</div>", unsafe_allow_html=True)

    # Main content area
    if not st.session_state.get('quiz_generated', False):
        display_welcome_screen()
    elif not st.session_state.get('show_results', False):
        display_quiz()
    else:
        display_results()

def display_welcome_screen():
    st.markdown("""
    <div class='glass-container animate-fade-in'>
        <h2>🌟 Welcome to Future Quiz AI</h2>
        <p>Experience the next generation of learning:</p>
        <ul>
            <li>🤖 AI-powered question generation</li>
            <li>📊 Real-time performance analytics</li>
            <li>🎯 Adaptive difficulty scaling</li>
            <li>⚡ Interactive learning assistance</li>
        </ul>
        <p>Ready to begin your journey? Configure your quiz in the Control Center!</p>
    </div>
    """, unsafe_allow_html=True)

def display_quiz():
    # Progress tracking
    progress = (st.session_state.current_question + 1) / len(st.session_state.questions)
    st.markdown(f"""
    <div class='progress-container'>
        <div class='progress-bar' style='width: {progress * 100}%'></div>
    </div>
    <p style='text-align: center; color: var(--text);'>
        Question {st.session_state.current_question + 1} of {len(st.session_state.questions)}
    </p>
    """, unsafe_allow_html=True)
    
    current_q = st.session_state.questions[st.session_state.current_question]
    
    # Question display with animation
    st.markdown(f"""
    <div class='glass-container animate-fade-in'>
        <h3 style='color: var(--text);'>❓ {current_q['mcq']}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Options in a grid
    col1, col2 = st.columns(2)
    options = [
        ('A', current_q['options']['a'], col1),
        ('B', current_q['options']['b'], col2),
        ('C', current_q['options']['c'], col1),
        ('D', current_q['options']['d'], col2)
    ]
    
    for letter, option, col in options:
        with col:
            if st.button(
                f"{letter}) {option}",
                use_container_width=True,
                key=f"option_{letter}"
            ):
                handle_answer(letter.lower(), current_q)

def handle_answer(selected_option, question):
    # Calculate time taken
    time_taken = time.time() - st.session_state.start_time
    
    # Update statistics
    st.session_state.session_data['total_questions_answered'] += 1
    st.session_state.session_data['average_time_per_question'] = (
        (st.session_state.session_data['average_time_per_question'] * 
         (st.session_state.session_data['total_questions_answered'] - 1) + time_taken) /
        st.session_state.session_data['total_questions_answered']
    )
    
    if selected_option == question['correct']:
        st.session_state.score += 1
        st.session_state.session_data['correct_answers'] += 1
        st.session_state.session_data['current_streak'] += 1
        st.session_state.session_data['best_streak'] = max(
            st.session_state.session_data['best_streak'],
            st.session_state.session_data['current_streak']
        )
        st.success("✨ Excellent Choice!")
    else:
        st.session_state.session_data['current_streak'] = 0
        st.error(f"💫 The correct answer was: {question['options'][question['correct']]}")
    
    # Move to next question or show results
    if st.session_state.current_question < len(st.session_state.questions) - 1:
        st.session_state.current_question += 1
        st.session_state.start_time = time.time()
    else:
        st.session_state.show_results = True
    st.rerun()

def display_results():
    total_questions = len(st.session_state.questions)
    score_percentage = (st.session_state.score / total_questions) * 100
    
    st.markdown(f"""
    <div class='glass-container animate-fade-in'>
        <h2 style='text-align: center; color: var(--text);'>
            🎉 Challenge Complete!
        </h2>
        <div class='stats-card'>
            <span>Final Score</span>
            <span>{st.session_state.score}/{total_questions} ({score_percentage:.1f}%)</span>
        </div>
        <div class='stats-card'>
            <span>Average Time</span>
            <span>{st.session_state.session_data['average_time_per_question']:.1f}s per question</span>
        </div>
        <div class='stats-card'>
            <span>Current Streak</span>
            <span>{st.session_state.session_data['current_streak']} questions</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("� Try Another Challenge", use_container_width=True):
            st.session_state.quiz_generated = False
            st.session_state.current_question = 0
            st.session_state.score = 0
            st.session_state.show_results = False
            st.rerun()
    with col2:
        if st.button("📊 View Detailed Analytics", use_container_width=True):
            st.session_state.show_analytics = True

if __name__ == "__main__":
    main()