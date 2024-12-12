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
        st.session_state.shown_order = []
        st.session_state.selected_ui = None

    if st.session_state.unused_ui:
        st.session_state.selected_ui = random.choice(st.session_state.unused_ui)
        st.session_state.unused_ui.remove(st.session_state.selected_ui)
        st.session_state.shown_order.append(st.session_state.selected_ui)
    else:
        st.session_state.unused_ui = UI_OPTIONS.copy()
        pick_ui()


def show_thinking_animation():
    st.write("Generating Output: Thinking...")
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.12)  # Reduced sleep time for smoother progress
        my_bar.progress(percent_complete + 1)
    st.write("Done!")



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

    if st.session_state['first_answer_ui_chosen']:
        st.session_state['first_answer_ui_chosen'] = False


def display_question_ui(current_question):
    apply_theme_to_question()
    st.markdown(f'<div class="my-container">{current_question.question}</div>', unsafe_allow_html=True)

def display_question(current_question):
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
def display_button(current_question, question_key, round_num, q_index):
    # Initialize session states
    if f"show_output2_button_{round_num}_{q_index}" not in st.session_state:
        st.session_state[f"show_output2_button_{round_num}_{q_index}"] = False

    if f"show_output1_{round_num}_{q_index}" not in st.session_state:
        st.session_state[f"show_output1_{round_num}_{q_index}"] = False
    if f"show_output2_{round_num}_{q_index}" not in st.session_state:
        st.session_state[f"show_output2_{round_num}_{q_index}"] = False

    # Randomly decide which output gets thinking animation
    if f"thinking_output_{round_num}_{q_index}" not in st.session_state:
        st.session_state[f"thinking_output_{round_num}_{q_index}"] = random.choice([1, 2])

    # First button for Output 1
    if st.button(f"Generate 1st Output", key=f"output1_button_{round_num}_{q_index}"):
        if st.session_state[f"thinking_output_{round_num}_{q_index}"] == 1 and question_key not in st.session_state['thinking_shown']:
            show_thinking_animation()
            st.session_state['thinking_shown'][question_key] = True
        st.session_state[f"show_output1_{round_num}_{q_index}"] = True
        st.session_state[f"show_output2_button_{round_num}_{q_index}"] = True

    # Display Output 1 if generated
    if st.session_state[f"show_output1_{round_num}_{q_index}"]:
        st.write(f"**Output 1:** {current_question.answers_without_o1}")

        # Second button for Output 2
        if st.session_state[f"show_output2_button_{round_num}_{q_index}"]:
            if st.button(f"Generate 2nd Output", key=f"output2_button_{round_num}_{q_index}"):
                if st.session_state[f"thinking_output_{round_num}_{q_index}"] == 2 and question_key not in st.session_state['thinking_shown']:
                    show_thinking_animation()
                    st.session_state['thinking_shown'][question_key] = True
                st.session_state[f"show_output2_{round_num}_{q_index}"] = True

    # Display Output 2 if generated
    if st.session_state[f"show_output2_{round_num}_{q_index}"]:
        st.write(f"**Output 2:** {current_question.answers_with_o1}")

    # Add the "Click to see the questions" button after both outputs are generated
    if st.session_state[f"show_output1_{round_num}_{q_index}"] and st.session_state[f"show_output2_{round_num}_{q_index}"]:
        if f"show_questions_button_{round_num}_{q_index}" not in st.session_state:
            st.session_state[f"show_questions_button_{round_num}_{q_index}"] = False

        if not st.session_state[f"show_questions_button_{round_num}_{q_index}"]:
            if st.button("Click to see the questions", key=f"show_questions_button_key_{round_num}_{q_index}"):
                st.session_state[f"show_questions_button_{round_num}_{q_index}"] = True
