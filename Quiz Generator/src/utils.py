import os
from openai import OpenAI
import streamlit as st

client = OpenAI(api_key=os.environ.get("API_KEY"),project=os.environ.get("PROJECT"))

QUIZ_CATEGORIES = ("Geography"
"History",
"Sports",
"Animals",
"Geography",
"Literature",
"TV",
"Fashion" ,
"History",
"Movies",
"Music",
"Religion")


def init_session():
    if 'quiz' not in st.session_state:
        st.session_state['quiz'] = None

    if 'score' not in st.session_state:
        st.session_state['score'] = 0

    if 'submitted' not in st.session_state:
        st.session_state['submitted'] = False

    if 'wrong_answers' not in st.session_state:
        st.session_state['wrong_answers'] = []

def generate_quiz(guiz_categoery_option,guiz_difficulty_option,quiz_type,number_of_questions):
    response = client.chat.completions.create(
         model="gpt-3.5-turbo",
        messages=[
                    {"role": "system", "content": '''Generate a JSON list response for a trivia questions depending on the number
                        and category, including the question,options, correct answer.
                        The format should be as follows:
                    [{
                    "question": "The actual question text goes here?",
                    "options": ["Option1", "Option2", "Option3", "Option4"],
                    "correctAnswer": "TheCorrectAnswer"
                    }]'''},
                    {"role": "user", "content": f"Generate {number_of_questions} {guiz_difficulty_option} {quiz_type} questions, for {guiz_categoery_option} category "}
                    ]
            )
    return response.choices[0].message.content
