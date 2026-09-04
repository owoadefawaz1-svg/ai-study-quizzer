import streamlit as st
import google.generativeai as genai
import json

# Setup the AI
API_KEY = 'AQ.Ab8RN6Iy_P3aJYOKvJ2KqSTEpa5qUq_eVCXZCoHfxQBH0svQIw' 
genai.configure(api_key=API_KEY)

# Educational System Prompt
system_instruction = """
You are an expert educator. Generate a 3-question multiple-choice quiz.
ONLY output valid JSON. No markdown, no extra text.
Structure: {"topic": "...", "questions": [{"question_text": "...", "options": ["A", "B", "C", "D"], "correct_answer": "...", "explanation": "..."}]}
"""
model = genai.GenerativeModel("gemini-1.5-flash", system_instruction=system_instruction)

# Build the Website UI
st.set_page_config(page_title="AI Study Quizzer", page_icon="🎓")
st.title(" AI Study Quizzer")
st.markdown("Welcome! Enter a topic you are studying for your external exams, and our AI will generate a custom quiz for you.")

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    topic = st.text_input("What are you studying?", placeholder="e.g., Photosynthesis")
    difficulty = st.selectbox("Select Difficulty:", ["Middle School", "High School", "University"])
    generate_btn = st.button("🚀 Generate Quiz")

# Main area for the quiz
if generate_btn and topic:
    with st.spinner(f"🤖 AI is creating a {difficulty} quiz on {topic}..."):
        prompt = f"Generate a 3-question multiple-choice quiz on '{topic}' for a {difficulty} level."
        response = model.generate_content(prompt)
        
        # Clean and parse JSON
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        try:
            quiz_data = json.loads(clean_text)
            st.session_state.quiz = quiz_data
        except:
            st.error("The AI got confused. Please try again!")

# Display the quiz if it exists
if 'quiz' in st.session_state:
    quiz = st.session_state.quiz
    st.subheader(f"📚 Topic: {quiz['topic'].title()}")
    
    for i, q in enumerate(quiz['questions']):
        st.markdown(f"**Question {i+1}: {q['question_text']}**")
        
        user_choice = st.radio(
            f"Select your answer for Q{i+1}:", 
            q['options'], 
            key=f"q_{i}",
            index=None
        )
        
        if user_choice == q['correct_answer']:
            st.success("✅ Correct!")
        elif user_choice is not None:
            st.error(f"❌ Incorrect. The answer was: {q['correct_answer']}")
            
        if user_choice is not None:
            st.info(f"💡 Explanation: {q['explanation']}")
        
        st.divider()
