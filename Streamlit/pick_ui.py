# pick_ui.py
import streamlit as st

import random
import time
from config import apply_theme_to_question

# Define all possible UI options
UI_OPTIONS = [0, 1]


# Function to pick a UI from unused options
def pick_ui():
    if "unused_ui" not in st.session_state:
        st.session_state.unused_ui = UI_OPTIONS.copy()
        st.session_state.shown_order = []  # To track the order UIs are displayed

    if st.session_state.selected_ui is not None and st.session_state.selected_ui in st.session_state.unused_ui:
        st.session_state.unused_ui.remove(st.session_state.selected_ui)

    if st.session_state.unused_ui:
        st.session_state.selected_ui = random.choice(st.session_state.unused_ui)
        st.session_state.unused_ui.remove(st.session_state.selected_ui)
        st.session_state.shown_order.append(st.session_state.selected_ui)

    else:
        # Reset unused options when all are used
        st.session_state.unused_ui = UI_OPTIONS.copy()
        pick_ui()


def show_thinking_animation():
    """Display the thinking animation and mark it as shown."""

    progress_text = "Generating Output Option with O1: Thinking..."

    round_num = st.session_state['current_round']
    q = st.session_state['current_question_within_round']  # 0: question #1, 1: question #2

    empty_space = st.empty()

    with empty_space.container():
        with st.status("Processing data...", expanded=True) as status:
            my_bar = st.progress(0)
            for percent_complete in range(100):
                time.sleep(0.15)
                my_bar.progress(percent_complete + 1)

            # st.write("Done!")
            status.update(label="Done!", state="complete")



# UI display functions
def display_ui_without_o1(current_question):
    st.write("Option Without O1:")
    response_text_update(current_question.answers_without_o1)


def display_ui_with_o1(current_question):
    # Show thinking animation only once per question
    if current_question.question_key not in st.session_state['thinking_shown']:
        show_thinking_animation()

        st.session_state['thinking_shown'][current_question.question_key] = True

    # Display GPT 4o Output 2
    response_text_update(current_question.answers_with_o1)


def display_selected_ui(current_question, question_key):
    if not st.session_state['first_answer_ui_chosen']:
        pick_ui()

    # Remove the automatic display of outputs
    if st.session_state['first_answer_ui_chosen']:
        st.session_state['first_answer_ui_chosen'] = False


def display_question_ui(current_question):
    apply_theme_to_question()
    st.markdown(f'<div class="my-container">{current_question.question}</div>', unsafe_allow_html=True)


def response_text_update(text, delay=0.001):
    # print one character at a time
    round_num = st.session_state['current_round']
    q = st.session_state['current_question_within_round']  # 0: question #1, 1: question #2
    s_ui = st.session_state.selected_ui

    if s_ui == 0:
        text_key = f"update_text_{round_num}_q_{q}_without_o1"
    else:  # s_ui = 1
        text_key = f"update_text_{round_num}_q_{q}_with_o1"

    placeholder = st.empty()
    displayed_text = ""

    for char in text:
        displayed_text += char
        placeholder.text(displayed_text)
        time.sleep(delay)
