import streamlit as st

from questions import questions_and_answers, submit_to_google_form, save_response_locally

import logging


# submit button
def submit_button_callback():
    q = st.session_state['current_question_within_round']  # question 0 or 1 within the round
    round_num = st.session_state['current_round']

    index = st.session_state['index_of_current_question']

    current_question = questions_and_answers[index]

    # Update current_question with submitted form responses
    response_preference_key = f'response_preference_{round_num}_{q + 1}'
    response_preference = st.session_state.get(response_preference_key, None)
    current_question.response_preference = st.session_state.response_preference

    relevance_preference_key = f'relevance_preference_{round_num}_{q + 1}'
    relevance_preference = st.session_state.get(relevance_preference_key, None)
    current_question.relevance_preference = st.session_state.relevance_preference

    validity_preference_key = f'validity_preference_{round_num}_{q + 1}'
    validity_preference = st.session_state.get(validity_preference_key, None)
    current_question.validity_preference = st.session_state.validity_preference

    explainability_preference_key = f'explainability_preference_{round_num}_{q + 1}'
    explainability_preference = st.session_state.get(explainability_preference_key, None)
    current_question.explainability_preference = st.session_state.explainability_preference

    response_data = {
        'round': round_num,
        'question': q + 1,
        'preference': st.session_state.response_preference,
        'relevance_preference': st.session_state.relevance_preference,
        'validity_preference': st.session_state.validity_preference,
        'explainability_preference': st.session_state.explainability_preference
    }

    # Submit to Google Form
    #submit_to_google_form(response_data)
    #st.session_state['responses'].append(response_data)

    # Empty placeholders to empty page
    st.session_state.placeholder_question.empty()
    st.session_state.placeholder_first_answer.empty()
    st.session_state.placeholder_second_answer.empty()
    st.session_state.placeholder_feedback.empty()

    # Move to next question or round
    if q == 1:
        logging.info(f"round: {round_num}, q: {q}")
        if st.session_state['current_round'] + 1 < 4:
            st.session_state['current_round'] += 1
        else:
            logging.info(f"round: {round_num}, q: {q}")
            st.session_state.stage = 2
        st.session_state['current_question_within_round'] = 0
    else:
        logging.info(f"round: {round_num}, q: {q}")
        st.session_state['current_question_within_round'] = 1



# sliders
def update_relevance_slider(widget_key, state_key):
    st.session_state[state_key] = st.session_state[widget_key]
