import streamlit as st

import time

import requests

from questions import questions_and_answers, submit_to_google_form, save_response_locally
# import random
from pick_ui import *
from config import themes, themes2, change_theme, theme_selection, initialize_theme
# from config import *


from streamlit.components.v1 import html

# Define study constants

NUM_ROUNDS = 3


def submit_button_callback():
    q = st.session_state['current_question_within_round']  # question 0 or 1 within the round
    round_num = st.session_state['current_round']

    current_question = st.session_state['current_question']

    # Update current_question with submitted form responses
    response_preference_key = f'response_preference_{round_num}_{q + 1}'
    current_question.response_preference = st.session_state.get(response_preference_key, None)

    relevance_preference_key = f'relevance_preference{round_num}_{q + 1}'
    current_question.relevance_preference = st.session_state.get(relevance_preference_key, None)

    validity_preference_key = f'validity_preference_{round_num}_{q + 1}'
    current_question.validity_preference = st.session_state.get(validity_preference_key, None)

    explainability_preference_key = f'explainability_preference_{round_num}_{q + 1}'
    current_question.explainability_preference = st.session_state.get(explainability_preference_key, None)

    response_data = {
        'round': round_num,
        'question': q + 1,
        'preference': current_question.response_preference,
        'relevance_preference': current_question.sliders[q].relevance_preference,
        'validity_preference': current_question.sliders[q].validity_preference,
        'explainability_preference': current_question.sliders[q].explainability_preference
    }

    # Submit to Google Form
    submit_to_google_form(st, response_data)
    st.session_state['responses'].append(response_data)

    # Move to next question or round
    if q == 1:
        st.session_state['current_round'] += 1
        st.session_state['current_question_within_round'] = 0
    else:
        st.session_state['current_question_within_round'] = 1

    # st.session_state.show_content = not st.session_state.show_content
    st.session_state.placeholder_feedback.empty()


def display_question_with_button(question, question_key, round_num, q_index, answers):

    if st.button(f"Show GPT 4o Output 1 (Question {q_index + 1})", key=f"output1_button_{round_num}_{q_index}"):
        st.write(answers[q_index][0])

    if st.button(f"Show GPT 4o Output 2 (Question {q_index + 1})", key=f"output2_button_{round_num}_{q_index}"):
        if question_key not in st.session_state['thinking_shown']:
            show_thinking_animation()
            st.session_state['thinking_shown'][question_key] = True
        st.write(answers[q_index][1])


def display_sliders_collect_responses(current_question, q, round_num):
    # Collect responses
    st.write("Please provide your responses below:")

    current_question.response_preference = st.radio(f"Round {round_num} Question {q + 1} Preference",
                                                    options=['1', '2'],
                                                    key=f'response_preference_{round_num}_{q + 1}')

    # Your existing sliders for relevance, validity, and explainability...
    current_question.sliders[q].relevance_preference = st.slider(
        f"GPT 4o Output 1 Relevance (1=Greater relevance in first response, 5=Greater relevance in second response)",
        min_value=1, max_value=5, value=3, key=f'relevance_preference{round_num}_{q + 1}'
    )

    current_question.sliders[q].validity_preference = st.slider(
        f"GPT 4o Output 1 Validity (1=Greater validity in first response, 5=Greater validity in second response)",
        min_value=1, max_value=5, value=3, key=f'validity_preference_{round_num}_{q + 1}'
    )

    current_question.sliders[q].explainability_preference = st.slider(
        f"GPT 4o Output 1 Explainability (1=Greater explainability in first response, 5=Greater explainability in second response)",
        min_value=1, max_value=5, value=3, key=f'explainability_preference_{round_num}_{q + 1}'
    )

    #if st.button('Submit Response', key=f'submit_{round_num}_{q + 1}'):
     #   submit_button_callback()

    st.button("Submit Response", key=f'submit_{round_num}_{q + 1}', on_click=submit_button_callback)


def start_questioning():
    # If the survey is started, begin showing questions
    if st.session_state['survey_started']:
        round_num = st.session_state['current_round']
        q = st.session_state['current_question_within_round']  # 0: with 01, 1: without o1
        with_or_without_o1 = st.session_state['selected_ui']

        # Create an empty container
        # placeholder = st.empty()

        st.markdown(f"### Round {round_num}")
        # st.write("Round ", round_num)

        # Calculate question index for current question in the round
        start_index = (round_num - 1) * 2
        q_index = start_index + q  # The index for the current question

        if q_index < len(questions_and_answers):  # Ensure within bounds

            current_question = st.session_state['remaining_questions'][q_index]

            if with_or_without_o1 == 0:
                question_key = f"round_{round_num}_q_{q}_without_o1"
            else:  # with_or_without_o1 == 1
                question_key = f"round_{round_num}_q_{q}_with_o1"

            current_question.question_key = question_key

            st.markdown(f"#### Question {q + 1}")
            # st.write("Question ", q + 1)


            display_button(current_question, question_key, round_num, q_index, answers)


            # st.write(current_question.question)
            display_question(current_question)

            display_selected_ui(current_question, question_key)

            # st.session_state.show_content = True

            # if 'placeholder_feedback' not in st.session_state:
            st.session_state.placeholder_feedback = st.empty()

            # if st.session_state.show_content:
            with st.session_state.placeholder_feedback.container():
                display_sliders_collect_responses(current_question, q, round_num)


def intro_statement():
    st.header('CS 197 Project :computer:', divider='blue')

    st.subheader(':green[Introduction]')

    st.write(
        "This study explores whether user perception of AI responses changes when responses include language suggesting that the AI 'thought' about the answer. Please read both AI responses and answer the questions accordingly. :sunglasses::sunglasses:")

    theme_selection()

    # Preliminary button

    if not st.session_state['preliminaries_done']:
        if st.button('Ready to start?'):
            st.session_state['preliminaries_done'] = True
            st.success('Ready to commence.')
            st.session_state['refresh_key'] = not st.session_state.get('refresh_key', False)  # Toggle key to proceed

    # Survey start button
    elif not st.session_state['survey_started']:
        if st.button('Double Click here to start survey'):
            st.session_state['survey_started'] = True
            st.session_state['refresh_key'] = not st.session_state['refresh_key']

    # Main experiment loop

    else:

        st.subheader(":red[Welcome to the Research Study]")

        st.write(f"You will be presented with {NUM_ROUNDS} rounds of questions.")

        st.write("Each round will show you 2 different questions with corresponding answers.")

        start_questioning()

        # After all rounds are completed

        if st.session_state['current_round'] > NUM_ROUNDS:
            st.success("Thank you for participating in the study!")

            st.write("You can now close this tab.")


def main():
    st.set_page_config(page_title="O1 Study", page_icon="🎨")

    # Initialize session states
    if "themes" not in st.session_state:
        st.session_state.themes = themes

    if "current_theme" not in st.session_state:
        st.session_state.current_theme = st.session_state.themes["current_theme"]

    initialize_theme()

    if 'preliminaries_done' not in st.session_state:
        st.session_state['preliminaries_done'] = False

    if 'survey_started' not in st.session_state:
        st.session_state['survey_started'] = False

    if 'thinking_shown' not in st.session_state:
        st.session_state['thinking_shown'] = {}

    if 'remaining_questions' not in st.session_state:
        st.session_state['remaining_questions'] = random.sample(questions_and_answers, len(questions_and_answers))

    if 'current_round' not in st.session_state:
        st.session_state['current_round'] = 1

    if 'current_question_within_round' not in st.session_state:  # question 0 or 1 of each round
        st.session_state['current_question_within_round'] = 0

    if 'current_question' not in st.session_state:  # question within the list
        st.session_state['current_question'] = st.session_state['remaining_questions'][0]  # first question

    if 'selected_ui' not in st.session_state:  # answer with or without o1
        st.session_state['selected_ui'] = random.choice([0, 1])
        if 'first_answer_ui_chosen' not in st.session_state:
            st.session_state['first_answer_ui_chosen'] = True

    if 'responses' not in st.session_state:
        st.session_state['responses'] = []

    if "show_content" not in st.session_state:
        st.session_state.show_content = True

    if 'stage' not in st.session_state:
        st.session_state.stage = 0

    intro_statement()


if __name__ == '__main__':
    main()
