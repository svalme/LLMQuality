# pick_ui.py
#import streamlit as st

import random
import time


# Define all possible UI options
UI_OPTIONS = [1, 2]

# Function to pick a UI from unused options
def pick_ui(session_state):
    if "unused_ui" not in session_state:
        session_state.unused_ui = UI_OPTIONS.copy()
        session_state.shown_order = []  # To track the order UIs are displayed
        session_state.selected_ui = None

    if session_state.unused_ui:
        session_state.selected_ui = random.choice(session_state.unused_ui)
        session_state.unused_ui.remove(session_state.selected_ui)
        session_state.shown_order.append(session_state.selected_ui)
    else:
        # Reset unused options when all are used
        session_state.unused_ui = UI_OPTIONS.copy()
        pick_ui(session_state)

def show_thinking_animation(st):
    """Display the thinking animation and mark it as shown."""
    st.write("Generating GPT 4o Output 2: Thinking...")
    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.15)

        my_bar.progress(percent_complete + 1)

    st.write("Done!")

# UI display functions
def display_ui_without_o1(st, current_question):
    # Display GPT 4o Output 1

    with st.expander("Click to see GPT 4o Output 1"):
        st.write(current_question.answers_without_o1)

def display_ui_with_o1(st, current_question, question_key):
    # Show thinking animation only once per question
    if question_key not in st.session_state['thinking_shown']:
        show_thinking_animation(st)

        st.session_state['thinking_shown'][question_key] = True

    # Display GPT 4o Output 2

    with st.expander("Click to see GPT 4o Output 2"):
        st.write(current_question.answers_with_o1)

def display_selected_ui(st, current_question, question_key):
    # display selected ui: a ui with or without thinking
    pick_ui(st.session_state)
    if st.session_state.selected_ui == 1:
        display_ui_without_o1(st, current_question)
    elif st.session_state.selected_ui == 2:
        display_ui_with_o1(st, current_question, question_key)

def response_text_update(st, text, delay=0.05):
    # print one character at a time
    placeholder = st.empty()
    displayed_text = ""

    for char in text:
        displayed_text += char
        placeholder.text(displayed_text)
        time.sleep(delay)

