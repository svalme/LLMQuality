import streamlit as st

import time

import requests

from questions import questions_and_answers, submit_to_google_form, save_response_locally
import random
from config import themes

from streamlit.components.v1 import html

# Define study constants

NUM_ROUNDS = 3


def response_text_update(text, delay=0.05):
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


def submit_button_callback():
    q = st.session_state['current_question_within_round']  # question 0 or 1 within the round
    round_num = st.session_state['current_round']

    current_question = st.session_state['current_question']

    # update current_question with submitted form responses
    response_preference_key = f'response_preference_{round_num}_{q + 1}'
    current_question.response_preference = st.session_state[response_preference_key]

    relevance_preference_key = f'relevance_preference{round_num}_{q + 1}'
    current_question.relevance_preference_key = st.session_state[relevance_preference_key]

    validity_preference_key = f'validity_preference_{round_num}_{q + 1}'
    current_question.validity_preference = st.session_state[validity_preference_key]

    explainability_preference_key = f'explainability_preference_{round_num}_{q + 1}'
    current_question.explainability_preference_key = st.session_state[explainability_preference_key]

    response_data = {
        'round': round_num,
        'question': q + 1,
        'preference': current_question.response_preference,
        'relevance_preference': current_question.sliders[q].relevance_preference,
        'validity_preference': current_question.sliders[q].validity_preference,
        'explainability_preference': current_question.sliders[q].explainability_preference
    }

    # Submit to Google Form
    submit_to_google_form(response_data)
    st.session_state['responses'].append(response_data)

    # Move to next question or round
    if q == 1:
        st.session_state['current_round'] += 1
        st.session_state['current_question_within_round'] = 0
    else:
        st.session_state['current_question_within_round'] = 1

    # st.rerun()


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

    st.button('Submit Response', on_click=submit_button_callback, key=f'submit_{round_num}_{q + 1}')

    # submit_button =
    # submit_button = st.form_submit_button('Submit Response', on_click=submit_button_callback, key=f'submit_{round_num}_{q + 1}')


def start_questioning():
    # If the survey is started, begin showing questions
    if st.session_state['survey_started']:
        round_num = st.session_state['current_round']
        q = st.session_state['current_question_within_round']  # 0: with 01, 1: without o1

        st.markdown(f"### Round {round_num}")

        # Calculate question index for current question in the round
        start_index = (round_num - 1) * 2
        q_index = start_index + q  # The index for the current question

        if q_index < len(questions_and_answers):  # Ensure within bounds

            current_question = st.session_state['remaining_questions'][q_index]

            question_key = f"round_{round_num}_q_{q}"
            current_question.question_key = question_key

            st.markdown(f"#### Question {q + 1}")

            response_text_update(current_question.question)

            #st.write(current_question.question)

            # Display GPT 4o Output 1

            with st.expander("Click to see GPT 4o Output 1"):
                st.write(current_question.answers_without_o1)

            # Show thinking animation only once per question
            if question_key not in st.session_state['thinking_shown']:
                show_thinking_animation()

                st.session_state['thinking_shown'][question_key] = True

            # Display GPT 4o Output 2

            with st.expander("Click to see GPT 4o Output 2"):

                st.write(current_question.answers_with_o1)

            display_sliders_collect_responses(current_question, q, round_num)


# Apply the theme using custom CSS
# Function to apply the selected theme's CSS dynamically
def apply_theme(theme_name):
    theme = themes[theme_name]  # Get the selected theme from the dictionary

    st.markdown(
        f"""
            <style>
            body {{
                background-color: {theme['backgroundColor']};
                color: {theme['textColor']};
            }}
            .css-1v3fvcr {{
                background-color: {theme['backgroundColor']};
                color: {theme['textColor']};
            }}
            .stButton>button {{
                background-color: {theme['primaryColor']};
                color: white;
            }}
            .stTextInput>div>div>input {{
                background-color: {theme['secondaryBackgroundColor']};
                color: {theme['textColor']};
            }}
            /*.stSelectbox>div>div>div {{
                background-color: {theme['secondaryBackgroundColor']};
                color: {theme['textColor']};
            }}*/
            </style>
            """,
        unsafe_allow_html=True
    )



    #st.rerun()

# Function to change theme
def change_theme():
    previous_theme = st.session_state.themes["current_theme"]
    tdict = st.session_state.themes["light"] if st.session_state.themes["current_theme"] == "light" else \
    st.session_state.themes["dark"]
    for vkey, vval in tdict.items():
        if vkey.startswith("theme"):
            st._config.set_option(vkey, vval)

    st.session_state.themes["refreshed"] = False
    if previous_theme == "dark":
        st.session_state.themes["current_theme"] = "light"
    elif previous_theme == "light":
        st.session_state.themes["current_theme"] = "dark"

def on_theme_change():
    # Store the selected theme in session state
    st.session_state.theme = st.session_state.theme_selectbox
    apply_theme(st.session_state.theme)
    #st.rerun()

def theme_selection():
    btn_face = st.session_state.themes["light"]["button_face"] if st.session_state.themes[
                                                                      "current_theme"] == "light" else \
        st.session_state.themes["dark"]["button_face"]
    st.button(btn_face, on_click=change_theme)

    if st.session_state.themes["refreshed"] == False:
        st.session_state.themes["refreshed"] = True
        st.rerun()


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
    # Initialize session states
   # if "theme" not in st.session_state:
   #     st.session_state.theme = "light"

    if "themes" not in st.session_state:
        st.session_state.themes = {
            "current_theme": "light",
            "refreshed": True,
            "light": {
                "theme.base": "dark",
                "theme.backgroundColor": "black",
                "theme.primaryColor": "#c98bdb",
                "theme.secondaryBackgroundColor": "#5591f5",
                "theme.textColor": "white",
                "button_face": "🌜"
            },
            "dark": {
                "theme.base": "light",
                "theme.backgroundColor": "white",
                "theme.primaryColor": "#5591f5",
                "theme.secondaryBackgroundColor": "#82E1D7",
                "theme.textColor": "#0a1464",
                "button_face": "🌞"
            }
        }

    st.set_page_config(page_title="O1 Study", page_icon="🎨")

    # Apply the current theme
    #apply_theme(themes[st.session_state.theme])
   # on_theme_change(themes[st.session_state.theme])

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

    if 'responses' not in st.session_state:
        st.session_state['responses'] = []

    intro_statement()




if __name__ == '__main__':
    main()