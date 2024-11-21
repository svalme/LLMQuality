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

def display_button(question, question_key, round_num, q_index, answers):
    # Create columns for buttons
    col1, col2 = st.columns(2)
    
    # Initialize session state for button visibility
    if f"show_output2_button_{round_num}_{q_index}" not in st.session_state:
        st.session_state[f"show_output2_button_{round_num}_{q_index}"] = False
    
    # Initialize session state for outputs
    if f"show_output1_{round_num}_{q_index}" not in st.session_state:
        st.session_state[f"show_output1_{round_num}_{q_index}"] = False
    if f"show_output2_{round_num}_{q_index}" not in st.session_state:
        st.session_state[f"show_output2_{round_num}_{q_index}"] = False

    with col1:
        if st.button(f"Generate First Output (Question {q_index + 1})", key=f"output1_button_{round_num}_{q_index}"):
            st.session_state[f"show_output1_{round_num}_{q_index}"] = True
            st.session_state[f"show_output2_button_{round_num}_{q_index}"] = True

    # Display first output if button was clicked
    if st.session_state[f"show_output1_{round_num}_{q_index}"]:
        st.write(answers[q_index][0])
        
        # Show second button after first output is displayed
        with col2:
            if st.session_state[f"show_output2_button_{round_num}_{q_index}"]:
                if st.button(f"Generate Second Output (Question {q_index + 1})", key=f"output2_button_{round_num}_{q_index}"):
                    # Only show thinking animation if not shown before for this question
                    if question_key not in st.session_state['thinking_shown']:
                        show_thinking_animation()
                        st.session_state['thinking_shown'][question_key] = True
                    st.session_state[f"show_output2_{round_num}_{q_index}"] = True

    # Display second output if its button was clicked
    if st.session_state[f"show_output2_{round_num}_{q_index}"]:
        st.write(answers[q_index][1])



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


def start_questioning():
    if st.session_state['survey_started']:
        round_num = st.session_state['current_round']
        q = st.session_state['current_question_within_round']
        with_or_without_o1 = st.session_state['selected_ui']

        st.markdown(f"### Round {round_num}")

        start_index = (round_num - 1) * 2
        q_index = start_index + q

        if q_index < len(questions_and_answers):
            current_question = st.session_state['remaining_questions'][q_index]

            question_key = f"round_{round_num}_q_{q}_{'with' if with_or_without_o1 else 'without'}_o1"
            current_question.question_key = question_key

            st.markdown(f"#### Question {q + 1}")
            display_question(current_question)
            display_button(current_question, question_key, round_num, q_index, answers)

            st.session_state.placeholder_feedback = st.empty()
            with st.session_state.placeholder_feedback.container():
                display_sliders_collect_responses(current_question, q, round_num)


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
