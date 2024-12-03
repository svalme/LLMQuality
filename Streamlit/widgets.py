import streamlit as st

from questions import submit_to_google_form

import logging


def validate_responses(round_num, q):
    """
    Validates that the user has provided all required responses (preferences and Likert scales).
    Returns True if all responses are filled, otherwise False.
    """
    response_preference_key = f'response_preference_{round_num}_{q + 1}'
    relevance_preference_key = f'relevance_preference_{round_num}_{q + 1}'
    validity_preference_key = f'validity_preference_{round_num}_{q + 1}'
    explainability_preference_key = f'explainability_preference_{round_num}_{q + 1}'

    return all([
        st.session_state.get(response_preference_key) is not None,
        st.session_state.get(relevance_preference_key) is not None,
        st.session_state.get(validity_preference_key) is not None,
        st.session_state.get(explainability_preference_key) is not None
    ])


# submit button
def submit_button_callback():
    q = st.session_state['current_question_within_round']
    round_num = st.session_state['current_round']
    current_question = st.session_state['current_question']

    # Initialize the warning placeholder if not already
    if f"warning_placeholder_{round_num}_{q}" not in st.session_state:
        st.session_state[f"warning_placeholder_{round_num}_{q}"] = st.empty()

    # Validate responses before submitting
    if not validate_responses(round_num, q):
        # Display warning at the bottom using the placeholder
        st.session_state[f"warning_placeholder_{round_num}_{q}"].warning("Please complete all responses before moving on to the next question.")
        return

    # Store responses if validation passes
    response_preference_key = f'response_preference_{round_num}_{q + 1}'
    current_question.response_preference = st.session_state.get(response_preference_key)

    relevance_preference_key = f'relevance_preference_{round_num}_{q + 1}'
    current_question.radio_buttons[q].relevance_preference = st.session_state.get(relevance_preference_key)

    validity_preference_key = f'validity_preference_{round_num}_{q + 1}'
    current_question.radio_buttons[q].validity_preference = st.session_state.get(validity_preference_key)

    explainability_preference_key = f'explainability_preference_{round_num}_{q + 1}'
    current_question.radio_buttons[q].explainability_preference = st.session_state.get(explainability_preference_key)

    # Prepare response data for submission
    response_data = {
        'round': round_num,
        'question': q + 1,
        'preference': current_question.response_preference,
        'relevance_preference': current_question.radio_buttons[q].relevance_preference,
        'validity_preference': current_question.radio_buttons[q].validity_preference,
        'explainability_preference': current_question.radio_buttons[q].explainability_preference
    }

    submit_to_google_form(response_data)
    st.session_state['responses'].append(response_data)

    # Transition to the next question or round
    if q == 1:
        st.session_state['current_round'] += 1
        st.session_state['current_question_within_round'] = 0
    else:
        st.session_state['current_question_within_round'] = 1

    st.session_state.placeholder_feedback.empty()
    st.success("Moving to the next question.")

def display_radio_buttons_collect_responses(current_question, q, round_num):
    st.write("Please provide your responses below:")

    current_question.response_preference = st.radio(
        f"Round {round_num} Question {q + 1} Preference",
        options=['1', '2'],
        index=None,
        key=f'response_preference_{round_num}_{q + 1}'
    )

    # Relevance Likert Scale (Horizontal layout)
    st.write("Relevance (1=Greater relevance in first response, 5=Greater relevance in second response)")
    current_question.radio_buttons[q].relevance_preference = st.radio(
        "Relevance Radio Button",
        options=[1, 2, 3, 4, 5],
        index=None, # No pre-filled selection
        horizontal=True, # Horizontal layout
        key=f'relevance_preference_{round_num}_{q + 1}',
        label_visibility="collapsed"
    )

    # Validity Likert Scale (Horizontal layout)
    st.write("Validity (1=Greater validity in first response, 5=Greater validity in second response)")
    current_question.radio_buttons[q].validity_preference = st.radio(
        "Validity Radio Button",
        options=[1, 2, 3, 4, 5],
        index=None, # No pre-filled selection
        horizontal=True, # Horizontal layout
        key=f'validity_preference_{round_num}_{q + 1}',
        label_visibility="collapsed"
    )

    # Explainability Likert Scale (Horizontal layout)
    st.write("Explainability (1=Greater explainability in first response, 5=Greater explainability in second response)")
    current_question.radio_buttons[q].explainability_preference = st.radio(
        "Explainability Radio Button",
        options=[1, 2, 3, 4, 5],
        index=None, # No pre-filled selection
        horizontal=True, # Horizontal layout
        key=f'explainability_preference_{round_num}_{q + 1}',
        label_visibility="collapsed"
    )
    st.button("Submit Response", key=f'submit_{round_num}_{q + 1}', on_click=submit_button_callback)

