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
        st.session_state.selected_ui = None

    if st.session_state.unused_ui:
        st.session_state.selected_ui = random.choice(st.session_state.unused_ui)
        st.session_state.unused_ui.remove(st.session_state.selected_ui)
        st.session_state.shown_order.append(st.session_state.selected_ui)
      #  if st.session_state['first_answer_ui_chosen']:
       #     st.session_state['first_answer_ui_chosen'] = False
    else:
        # Reset unused options when all are used
        st.session_state.unused_ui = UI_OPTIONS.copy()
        pick_ui()

def show_thinking_animation():
    """Display the thinking animation and mark it as shown."""
    st.write("Generating GPT 4o Output 2: Thinking...")
    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.15)

        my_bar.progress(percent_complete + 1)

    st.write("Done!")

# UI display functions
def display_ui_without_o1(current_question):
    # Display GPT 4o Output 1

    #with st.expander("Click to see GPT 4o Output 1"):
        #st.write(current_question.answers_without_o1)

    response_text_update(current_question.answers_without_o1)

def display_ui_with_o1(current_question, question_key):
    # Show thinking animation only once per question
    if question_key not in st.session_state['thinking_shown']:
        show_thinking_animation()

        st.session_state['thinking_shown'][question_key] = True

    # Display GPT 4o Output 2

    response_text_update(current_question.answers_with_o1)
    #with st.expander("Click to see GPT 4o Output 2"):
        #st.write(current_question.answers_with_o1)

def display_selected_ui(current_question, question_key):
    # display selected ui: a ui with or without thinking
    if not st.session_state['first_answer_ui_chosen']:
        pick_ui()

    if st.session_state.selected_ui == 0:
        display_ui_without_o1(current_question)
    elif st.session_state.selected_ui == 1:
        display_ui_with_o1(current_question, question_key)

    if st.session_state['first_answer_ui_chosen']:
        st.session_state['first_answer_ui_chosen'] = False

def display_question(current_question):
    apply_theme_to_question()
    #apply_theme_to_question()
    st.markdown(f'<div class="my-container">{current_question.question}</div>', unsafe_allow_html=True)
      #  st.write(current_question.question)


def response_text_update(text, delay=0.05):
    # print one character at a time
    placeholder = st.empty()
    displayed_text = ""

    for char in text:
        displayed_text += char
        placeholder.text(displayed_text)
        time.sleep(delay)

