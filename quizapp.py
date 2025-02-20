import streamlit as st
import json
import os
from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

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

def main():
    st.title("📝 AI-Powered Quiz Generator")

    # User input text
    text_content = st.text_area("📄 Paste the text content here:")

    # Dropdown for difficulty level
    quiz_level = st.selectbox("🎯 Select quiz difficulty:", ["Easy", "Medium", "Hard"])
    
    # Initialize session state
    session_state = st.session_state
    if "quiz_generated" not in session_state:
        session_state.quiz_generated = False

    # Generate quiz button
    if st.button("🚀 Generate Quiz"):
        session_state.quiz_generated = True
        session_state.questions = fetch_questions(text_content, quiz_level.lower())

    # Display quiz only if generated
    if session_state.quiz_generated and session_state.questions:
        st.subheader("🧠 Your Quiz:")
        selected_options = []
        correct_answers = []
        
        for question in session_state.questions:
            options = question["options"]
            selected = st.radio(question["mcq"], list(options.values()), index=None)
            selected_options.append(selected)
            correct_answers.append(options[question["correct"]])

        # Submit button
        if st.button("✅ Submit"):
            st.subheader("📊 Quiz Results:")
            marks = 0
            for i, question in enumerate(session_state.questions):
                st.write(f"**{question['mcq']}**")
                st.write(f"🔵 Your Answer: {selected_options[i]}")
                st.write(f"✅ Correct Answer: {correct_answers[i]}")
                if selected_options[i] == correct_answers[i]:
                    marks += 1

            st.success(f"🎉 You scored **{marks} / {len(session_state.questions)}**")

if __name__ == "__main__":
    main()