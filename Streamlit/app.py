import streamlit as st

import time

import requests

from questions import questions_and_answers, submit_to_google_form, save_response_locally
import random

# Define study constants

NUM_ROUNDS = 3


def response_text_update(text, delay=0.1):
    # print one character at a time
    placeholder = st.empty()
    displayed_text = ""

    for char in text:
        displayed_text += char
        placeholder.text(displayed_text)
        time.sleep(delay)


def show_thinking_animation():
    """Display the thinking animation and mark it as shown."""

    st.write("Generating GPT 4o Output 2: Thinking...")

    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.15)

        my_bar.progress(percent_complete + 1)

    st.write("Done!")


def display_sliders_collect_responses(q, round_num):
    # Collect responses
    st.write("Please provide your responses below:")
    preference = st.radio(f"Round {round_num} Question {q + 1} Preference", options=['1', '2'],
                          key=f'preference_{round_num}_{q + 1}')

    # Your existing sliders for relevance, validity, and explainability...
    relevance_preference = st.slider(
        f"GPT 4o Output 1 Relevance (1=Greater relevance in first response, 5=Greater relevance in second response)",
        min_value=1, max_value=5, value=3, key=f'relevance_preference{round_num}_{q + 1}'
    )

    validity_preference = st.slider(
        f"GPT 4o Output 1 Validity (1=Greater validity in first response, 5=Greater validity in second response)",
        min_value=1, max_value=5, value=3, key=f'validity_preference_{round_num}_{q + 1}'
    )

    explainability_preference = st.slider(
        f"GPT 4o Output 1 Explainability (1=Greater explainability in first response, 5=Greater explainability in second response)",
        min_value=1, max_value=5, value=3, key=f'explainability_preference_{round_num}_{q + 1}'
    )

    if st.button('Submit Response', key=f'submit_{round_num}_{q + 1}'):
        response_data = {
            'round': round_num,
            'question': q + 1,
            'preference': preference,
            'relevance_preference': relevance_preference,
            'validity_preference': validity_preference,
            'explainability_preference': explainability_preference
        }

        # Submit to Google Form
        submit_to_google_form(response_data)
        st.session_state['responses'].append(response_data)

        # Move to next question or round
        if q == 1:
            st.session_state['current_round'] += 1
            st.session_state['current_question'] = 0
        else:
            st.session_state['current_question'] = 1

        st.rerun()


def start_questioning():
    # If the survey is started, begin showing questions
    if st.session_state['survey_started']:
        round_num = st.session_state['current_round']
        q = st.session_state['current_question']

        st.markdown(f"### Round {round_num}")

        # Calculate question index for current question in the round
        start_index = (round_num - 1) * 2
        q_index = start_index + q  # The index for the current question

        if q_index < len(questions_and_answers):  # Ensure within bounds

            question_key = f"round_{round_num}_q_{q}"

            st.markdown(f"#### Question {q + 1}")

            st.write(st.session_state['remaining_questions'][q_index]["question"])

            # Display GPT 4o Output 1

            with st.expander("Click to see GPT 4o Output 1"):
                st.write(st.session_state['remaining_questions'][q_index]["answers"][0])

            # Show thinking animation only once per question
            if question_key not in st.session_state['thinking_shown']:
                show_thinking_animation()

                st.session_state['thinking_shown'][question_key] = True

            # Display GPT 4o Output 2

            with st.expander("Click to see GPT 4o Output 2"):

                st.write(st.session_state['remaining_questions'][q_index]["answers"][1])

            display_sliders_collect_responses(q, round_num)


def intro_statement():
    st.header('CS 197 Project :computer:', divider='blue')

    st.subheader(':green[Introduction]')

    st.write(
        "This study explores whether user perception of AI responses changes when responses include language suggesting that the AI 'thought' about the answer. Please read both AI responses and answer the questions accordingly. :sunglasses::sunglasses:")

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
    # Initialize session states

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

    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = 0

    if 'responses' not in st.session_state:
        st.session_state['responses'] = []

    intro_statement()


if __name__ == '__main__':
    main()
