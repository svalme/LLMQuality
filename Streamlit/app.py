# app.py

import streamlit as st
import random

from pick_ui import display_question, display_button
from questions import questions, answers, QuestionsAndAnswers
from widgets import display_radio_buttons_collect_responses

# Constants
NUM_ROUNDS = 3
UI_OPTIONS = [0, 1]


def start_questioning():
    if st.session_state['survey_started']:
        round_num = st.session_state['current_round']
        q = st.session_state['current_question_within_round']
        with_or_without_o1 = st.session_state['selected_ui']

        st.markdown(f"### Round {round_num}")
        start_index = (round_num - 1) * 2
        q_index = start_index + q

        # Use st.session_state['questions_and_answers'] instead of questions_and_answers
        if q_index < len(st.session_state['questions_and_answers']):
            current_question = st.session_state['remaining_questions'][q_index]
            question_key = f"round_{round_num}_q_{q}_{'with' if with_or_without_o1 else 'without'}_o1"
            current_question.question_key = question_key

            st.markdown(f"#### Question {q + 1}")
            display_question(current_question)
            display_button(current_question, question_key, round_num, q_index)

            # Check if the "Click to see the questions" button has been clicked
            show_questions_button_key = f"show_questions_button_{round_num}_{q_index}"
            show_questions = st.session_state.get(show_questions_button_key, False)

            if show_questions:
                if 'placeholder_feedback' not in st.session_state:
                    st.session_state.placeholder_feedback = st.empty()

                #st.session_state.placeholder_feedback.empty()
                with st.session_state.placeholder_feedback.container():
                    display_radio_buttons_collect_responses(current_question, q, round_num)
            else:
                # If the button has not been clicked yet, prompt the user to generate outputs
                if st.session_state[f"show_output1_{round_num}_{q_index}"] and st.session_state[f"show_output2_{round_num}_{q_index}"]:
                    st.info("After reading both outputs, please click the 'Click to see the questions' button to proceed.")

def survey_started_callback():
    st.session_state.survey_started = True

def intro_statement():
    st.header('CS 197 Project :computer:')
    st.subheader('Introduction')
    st.write(
        "This study explores whether user perception of AI responses changes when responses include language suggesting that the AI 'thought' about the answer. Please read both AI responses and answer the questions accordingly.")

    if not st.session_state['survey_started']:
        st.button('Ready to start?', on_click=survey_started_callback)
    else:
        st.subheader("Welcome to the Research Study")
        st.write(f"You will be presented with {NUM_ROUNDS} rounds of questions.")
        st.write("Each round will show you 2 different questions with corresponding answers.")

        start_questioning()

        if st.session_state['current_round'] > NUM_ROUNDS:
            st.success("Thank you for participating in the study!")
            st.write("You can now close this tab.")

def main():
    st.set_page_config(page_title="O1 Study", page_icon="🎨")

    # Initialize the questions_and_answers list before using it
    if 'questions_and_answers' not in st.session_state:
        questions_and_answers = []
        for i, question_text in enumerate(questions):
            question_and_answer = QuestionsAndAnswers(question_text, answers[i])
            questions_and_answers.append(question_and_answer)
        st.session_state['questions_and_answers'] = questions_and_answers

    session_state_vars = {
        'preliminaries_done': False,
        'survey_started': False,
        'thinking_shown': {},
        'remaining_questions': random.sample(st.session_state['questions_and_answers'],
                                             len(st.session_state['questions_and_answers'])),
        'current_round': 1,
        'current_question_within_round': 0,
        'selected_ui': random.choice(UI_OPTIONS),
        'responses': [],
        'show_content': True,
        'stage': 0
    }

    for var, value in session_state_vars.items():
        if var not in st.session_state:
            st.session_state[var] = value

    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = st.session_state['remaining_questions'][0]

    if 'first_answer_ui_chosen' not in st.session_state:
        st.session_state['first_answer_ui_chosen'] = True

    intro_statement()





if __name__ == '__main__':
    main()
