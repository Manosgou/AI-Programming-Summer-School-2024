import json
import time
import streamlit as st
from utils import QUIZ_CATEGORIES,generate_quiz, init_session


st.header('Quiz Generator', divider='red')

init_session()

guiz_categoery_option = st.selectbox(key=100,label='Selct category:',options=QUIZ_CATEGORIES,index=None)
guiz_difficulty_option= st.selectbox(key=200,label='Selct difficulty:',options=("Easy","Medium","Hard"),index=None)
quiz_type = st.selectbox(key=300,label="Select quiz type",options=("True/False","Multiple Choice"),index=None)
number_of_questions = st.slider("Select number of questions", 1, 10)
if st.button("Generate quiz",type="primary"):
    try:
        quiz = generate_quiz(guiz_categoery_option,guiz_difficulty_option,quiz_type,number_of_questions)
        if quiz:
            st.session_state['quiz'] = json.loads(quiz)
    except ValueError:
        pass

st.divider()
if st.session_state['quiz']:
    st.title(f"{guiz_categoery_option if guiz_categoery_option else ''} Quiz!")
    st.session_state['score'] = 0
    st.session_state['submitted'] = False
    st.session_state['wrong_answers'].clear()
    with st.form("quiz_form"):
        for index,question in enumerate(st.session_state['quiz'],1):
            st.markdown(f"**Question {index}:** {question.get('question')}")
            answer = st.selectbox(key=index,label='Selct category:',options=question.get('options'),index=None)
            if answer == question.get("correctAnswer"):
                st.session_state['score']+=1
                st.markdown(''':green[Correct Answer!] ''')
            elif answer is None:
                st.markdown(''':orange[Please select one of the available options]''')
                st.session_state['wrong_answers'].append(f"Question {index}")
            else:
                st.markdown(''':red[Wrong Answer! :(]''')
                st.session_state['wrong_answers'].append(f"Question {index}")
        if st.form_submit_button("Submit"):
            st.session_state['submitted'] = True

if st.session_state['submitted']:
    st.title("Results")
    score_bar = st.progress(0, text=f"Score:{st.session_state['score']}/{len(st.session_state['quiz'])}")
    for percent_complete in range(100):
        time.sleep(0.001)
        if percent_complete + 1 <=(st.session_state['score']/len(st.session_state['quiz']))*100:
            score_bar.progress(percent_complete + 1, text=f"Score:{st.session_state['score']}/{len(st.session_state['quiz'])}")
    if st.session_state['score'] == len(st.session_state['quiz']):
        st.balloons()
    else:
        st.write("Give the following questions a second try:")
        for question in st.session_state['wrong_answers']:
            st.markdown("- " + question)
