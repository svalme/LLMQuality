import streamlit as st

import time

import requests

# import random
from pick_ui import *
from config import themes, themes2, change_theme, theme_selection, initialize_theme
# from config import *
from widgets import *

from streamlit.components.v1 import html

# Define study constants

NUM_ROUNDS = 3

logging.basicConfig(level=logging.DEBUG)

def display_sliders_collect_responses(current_question, q, round_num):
    # if st.session_state.clear_flag:
    # st.session_state.placeholder_feedback.empty()  # Clear the container
    #    st.session_state.clear_flag = False  # Reset the flag

    with st.session_state.placeholder_feedback.container():
    #with st.container():
        # Collect responses
        st.write("Please provide your responses below:")
        #st.button("Submit Response", key='submit_button', on_click=submit_button_callback)

        response_label = f"Round {round_num} Question {q + 1} Preference"
        response_options = ['Without O1', 'With O1']
        response_preference_key = f'response_preference_{round_num}_{q + 1}'
        response_preference = st.radio(response_label, options=response_options, key=response_preference_key)
        current_question.response_preference = response_preference

        #st.write(f"current_question.response_preference: {current_question.response_preference}")

        # Your existing sliders for relevance, validity, and explainability...
        relevance_label = f"Relevance (1=Greater relevance in first response, 5=Greater relevance in second response)"
        relevance_preference_key = f'relevance_preference_{round_num}_{q + 1}'
        relevance_preference = st.slider(relevance_label, min_value=1, max_value=5, value=3, key=relevance_preference_key)
        current_question.sliders[q].relevance_preference = relevance_preference

        logging.info(f"current_question.sliders[q].relevance_preference: {current_question.sliders[q].relevance_preference}")


        validity_label = f"Validity (1=Greater validity in first response, 5=Greater validity in second response)"
        validity_preference_key = 'validity_preference_{round_num}_{q + 1}'
        validity_preference = st.slider(validity_label, min_value=1, max_value=5, value=3, key=validity_preference_key)
        current_question.sliders[q].validity_preference = validity_preference

        logging.info(f"current_question.sliders[q].validity_preference: {current_question.sliders[q].validity_preference}")


        explainability_preference = f"Explainability (1=Greater explainability in first response, 5=Greater explainability in second response)"
        explainability_preference_key = 'explainability_preference_{round_num}_{q + 1}'
        explainability_preference = st.slider(explainability_preference, min_value=1, max_value=5, value=3, key=explainability_preference_key)
        current_question.sliders[q].explainability_preference = explainability_preference

        logging.info(f"current_question.sliders[q].validity_preference: {current_question.sliders[q].explainability_preference}")


        submit_button_key=f'submit_{round_num}_{q + 1}'
        st.button("Submit Response", key=submit_button_key, on_click=submit_button_callback)


def display_second_answer():
    #with st.container():
    with st.session_state.placeholder_second_answer.container():
        #with st.container():
        round_num = st.session_state['current_round']
        q = st.session_state['current_question_within_round']  # 0: question #1, 1: question #2
        with_or_without_o1 = st.session_state['selected_ui']

        # Create an empty container
        # placeholder = st.empty()

        # Calculate question index for current question in the round
        start_index = (round_num - 1) * 2
        q_index = start_index + q  # The index for the current question
        current_question = st.session_state['remaining_questions'][q_index]

    with st.container():
        display_selected_ui(current_question)


def display_first_answer():
    #with st.session_state.placeholder_first_answer.container():

    st.session_state.get('placeholder', st.empty()).empty()

    empty_space = st.empty()

    #with empty_space.container():

    with st.session_state.placeholder_first_answer.container():
        round_num = st.session_state['current_round']
        q = st.session_state['current_question_within_round']  # 0: question #1, 1: question #2

        if q not in [0, 1]:
            st.error(f"Invalid question index: {q}. Resetting to 0.")
            st.session_state['current_question_within_round'] = 0
            q = 0


        with_or_without_o1 = st.session_state['selected_ui']

        # Create an empty container
        # placeholder = st.empty()

        # Calculate question index for current question in the round
        start_index = (round_num - 1) * 2
        q_index = start_index + q  # The index for the current question

        if q_index < len(st.session_state['remaining_questions']):
            current_question = st.session_state['remaining_questions'][q_index]
            display_selected_ui(current_question)
        else:
            st.error(f"Question index {q_index} is out of range.")

        # question_key = f"round_{round_num}_q_{q}_without_o1"
   # st.session_state.get('placeholder', st.empty()).empty()
    #with st.container():
        #display_selected_ui(current_question)

       # with st.status("Processing data...", expanded=True) as status:
       #     st.write("Starting the process...")
       #     progress_bar = st.progress(0)

        #    for i in range(100):
        #        time.sleep(0.1)  # Simulating some work being done
        #        progress_bar.progress(i + 1)
        #        if i == 50:
        #            status.update(label="Halfway there!", state="running")

        #    status.update(label="Process complete!", state="complete")

        # st.session_state.show_content = True

        # if 'placeholder_feedback' not in st.session_state:
        #     st.session_state.placeholder_feedback = st.empty()
        # st.session_state.placeholder_feedback = st.empty()

        # if st.session_state.show_content:
        # with st.session_state.placeholder_feedback.container():
        # display_sliders_collect_responses(current_question, q, round_num)


def display_question():
    # If the survey is started, begin showing questions
    #with st.session_state.placeholder_question.container():

    with st.container():

    #with st.session_state.placeholder_question.container():
        round_num = st.session_state['current_round']
        q = st.session_state['current_question_within_round']  # 0: question #1, 1: question #2
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
            st.session_state.current_question = st.session_state['remaining_questions'][q_index]

            if with_or_without_o1 == 0:
                question_key = f"round_{round_num}_q_{q}_without_o1"
            else:  # with_or_without_o1 == 1
                question_key = f"round_{round_num}_q_{q}_with_o1"

            current_question.question_key = question_key

            st.markdown(f"#### Question {q + 1}")
            # st.write("Question ", q + 1)

            # st.write(current_question.question)
            display_question_ui(current_question)


def ending_statement(placeholder):
    #st.write("Display page")
    #st.session_state.placeholder_ending_statement = st.empty()
    # After all rounds are completed
    #with st.session_state.placeholder_ending_statement.container():
    with placeholder.container():
        #if st.session_state['current_round'] > NUM_ROUNDS:
        st.success("Thank you for participating in the study!")
        st.write("You can now close this tab.")

def display_survey():

    logging.debug("CONTENT")
    st.write("")

    display_question()
    #time.sleep(0.5)
    display_first_answer()
    display_second_answer()
    current_question = st.session_state['remaining_questions'][st.session_state.q_index]
    q = st.session_state['current_question_within_round']
    round_num = st.session_state['current_round']

    display_sliders_collect_responses(current_question, q, round_num)

def intro_statement(placeholder):
    with placeholder.container():
        theme_selection()
        st.header('CS 197 Project :computer:')
        st.markdown("---")
        st.subheader(':green[Introduction]')
        st.write(
            "This study explores whether user perception of AI responses changes when responses include language suggesting that the AI 'thought' about the answer. Please read both AI responses and answer the questions accordingly. :sunglasses::sunglasses:")

        st.write(f"You will be presented with {NUM_ROUNDS} rounds of questions.")
        st.write("Each round will show you 2 different questions with corresponding answers.")
        st.button("Start Survey", on_click=start_survey_button_callback)


def start_survey_button_callback():
    st.session_state['survey_started'] = True
    st.session_state.stage = 1
    st.session_state.main_placeholder.empty()

def next_stage():
    st.session_state.stage += 1


def choosePage():
    placeholder = st.session_state.main_placeholder

    if st.session_state.stage == 0:
        intro_statement(placeholder)

    elif st.session_state.stage == 1:
        display_survey()

    elif st.session_state.stage == 2:
        ending_statement(placeholder)


    elif st.session_state.stage == 3:
        with st.container():
            # demographics/background info
            if st.button("Continue"):
                st.session_state.stage = 4
                st.rerun()
    else:
        st.write("A session state stage with this value doesn't exist.")



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

    # questions

    if 'remaining_questions' not in st.session_state:
        st.session_state['remaining_questions'] = questions_and_answers

    if 'index_of_current_question' not in st.session_state:
        st.session_state['index_of_current_question'] = 0

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

    if 'q_index' not in st.session_state:
        st.session_state.q_index = 0

    # placeholders

    if 'main_placeholder' not in st.session_state:
        st.session_state['main_placeholder'] = st.empty()

    if 'placeholder_intro_statement' not in st.session_state:
        st.session_state.placeholder_intro_statement = st.empty()

    if 'placeholder_question' not in st.session_state:
        st.session_state.placeholder_question = st.empty()

    if 'placeholder_first_answer' not in st.session_state:
        st.session_state.placeholder_first_answer = st.empty()

    if 'placeholder_second_answer' not in st.session_state:
        st.session_state.placeholder_second_answer = st.empty()

    if 'placeholder_feedback' not in st.session_state:
        st.session_state.placeholder_feedback = st.empty()

    if 'placeholder_ending_statement' not in st.session_state:
        st.session_state.placeholder_ending_statement = st.empty()

    if 'clear_flag' not in st.session_state:
        st.session_state.clear_flag = False

    # radio button

    if 'response_preference' not in st.session_state:
        st.session_state.response_preference = 'Without O1'

    if 'response_preference_key' not in st.session_state:
        st.session_state['response_preference_key'] = None  # Default value

    # sliders default value
    if 'relevance_preference' not in st.session_state:
        st.session_state.relevance_preference = None

    if 'relevance_preference_key' not in st.session_state:
        st.session_state['relevance_preference_key'] = None  # Default value

    if 'validity_preference' not in st.session_state:
        st.session_state.validity_preference = None

    if 'validity_preference_key' not in st.session_state:
        st.session_state['validity_preference_key'] = None  # Default value

    if 'explainability_preference' not in st.session_state:
        st.session_state.explainability_preference = None

    if 'explainability_preference_key' not in st.session_state:
        st.session_state['explainability_preference_key'] = None  # Default value



    choosePage()


if __name__ == '__main__':
    main()
