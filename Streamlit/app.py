import streamlit as st
import random
import time
import requests
import pandas as pd
from datetime import datetime
import os
import csv

# Theme configuration
themes = {
    "current_theme": "light",
    "refreshed": True,
    "light": {
        "theme.base": "dark",
        "theme.primaryColor": "#000000",
        "theme.backgroundColor": "#FFFFFF",
        "theme.secondaryBackgroundColor": "#F0F2F6",
        "theme.textColor": "#0D0D0D",
        "button_face": "🌞",
        "containerBackground": "#F3F3F3"
    },
    "dark": {
        "theme.base": "light",
        "theme.primaryColor": "#b4b4b4",
        "theme.backgroundColor": "#212121",
        "theme.secondaryBackgroundColor": "#0E1117",
        "theme.textColor": "#ECECEC",
        "button_face": "🌜",
        "containerBackground": "#303030"
    }
}

# Questions and Answers Data
questions = [
    "Laird: Pure research provides us with new technologies that contribute to saving lives. Even more worthwhile than this, however, is its role in expanding our knowledge and providing new, unexplored ideas. Kim: Your priorities are mistaken. Saving lives is what counts most of all. Without pure research, medicine would not be as advanced as it is. Laird and Kim disagree on whether pure research: (A) derives its significance from new technologies, (B) expands our knowledge of medicine, (C) should prioritize saving lives, (D) has its value in medical applications, or (E) has value only in providing technologies to save lives?",
    "Executive: We recently ran a set of advertisements in a travel magazine and on its website. We were unable to get direct information about consumer response to the print ads. However, we found that consumer response to the website ads was much more limited than typical. We concluded that consumer response to the print ads was probably below par. The executive’s reasoning does which one of the following? (A) base a prediction on information about intensity of a phenomenon’s cause, (B) use typical frequency to draw conclusions about a particular event, (C) infer a statistical generalization from specific instances, (D) use a case with direct evidence to draw conclusions about an analogous case, or (E) base a prediction on facts about recent comparable events?",
    "During the construction of the Quebec Bridge in 1907, designer Theodore Cooper learned of a downward deflection of the span. Before he could act, the cantilever arm broke, causing the worst construction disaster in history. The inquiry that followed changed the engineering rules of thumb used worldwide. Which one of the following can be inferred from the passage? (A) Bridges built before 1907 were unsafe due to lack of analysis, (B) Cooper’s absence caused the cantilever to break, (C) Engineers relied on rules of thumb due to inadequate methods, (D) Only rigorous analysis could have prevented the collapse, or (E) Prior to 1907, mathematical analysis was insufficient for safety.",
    "The supernova event of 1987 is notable for the absence of the neutron star that should have remained after such an explosion, despite extensive searches for its radiation. Thus, current theory claiming that certain supernovas always produce neutron stars is likely incorrect. Which one of the following strengthens the argument? (A) Most detected remnants have a nearby neutron star, (B) Neutron stars have been found farther away than the 1987 location, (C) The 1987 supernova was the first observed in progress, (D) Several features of the supernova match current theory, or (E) Some neutron stars arise from causes other than supernovae.",
    "Political scientist: Democracy does not promote political freedom; historical examples show democracies can lead to oppression, while some despotisms provide freedom. The reasoning is flawed because it (A) confuses necessary with sufficient conditions for freedom, (B) fails to consider that increased freedom might lead to more democracy, (C) appeals to irrelevant historical examples, (D) overlooks that democracy can promote freedom without being necessary or sufficient, or (E) bases its case on a personal viewpoint.",
    "Journalist: To balance the need for profits to support drug research with the moral imperative to provide medicines to those in need, some pharmaceutical companies sell drugs at high prices in rich nations and lower prices in poor ones. This practice is unjustified. Which principle most helps to justify the journalist’s reasoning? (A) The ill deserve more consideration than the healthy, (B) Wealthy institutions must use resources to assist the incapable, (C) Special consideration depends on needs rather than societal characteristics, (D) People in wealthy nations shouldn't have better healthcare than those in poorer nations, or (E) Unequal access to healthcare is more unfair than unequal wealth distribution.",
]

# Define answers (GPT 4o)
answers = {
    0: [
        "Laird and Kim have contrasting views on the value of pure research, with Laird focusing on the intrinsic worth of expanding knowledge and sparking new ideas, while Kim prioritizes its life-saving applications. Laird argues that pure research should not be confined to practical applications but valued for fostering intellectual growth. Kim, on the other hand, sees the life-saving potential of pure research as the most significant aspect. The correct answer is (C), as their disagreement fundamentally revolves around whether pure research should prioritize saving lives over advancing knowledge for its own sake.",
        "Laird and Kim’s debate revolves around the value of pure research, with Laird emphasizing its role in expanding knowledge and generating new ideas, while Kim focuses on its life-saving applications. Laird argues that research has intrinsic worth by pushing the boundaries of human understanding, which he sees as more valuable than its immediate practical benefits. Kim, however, takes a pragmatic view, emphasizing the direct impact of research on medicine and its capacity to save lives. This fundamental disagreement points to (C), as they differ on whether pure research should prioritize life-saving outcomes over knowledge for knowledge’s sake.",
    ],
    1: [
        "The executive's reasoning infers consumer response to print ads based on the underwhelming response to digital ads in the same campaign. This assumption draws parallels between two advertising mediums within the same context without direct evidence from print media. The reasoning uses the digital response as an analogy to make inferences about print, which makes (D) the most accurate answer. The executive's argument relies on analogous evidence due to the lack of direct information on the print ads’ impact.",
        "The executive’s conclusion is based on limited consumer response to online advertisements, extrapolating that response levels to print ads were likely below par as well. The reasoning here involves inferring from an analogous case, as the executive uses data from one medium (online ads) to predict the results of another (print ads) within the same campaign context. Thus, (D) is the correct answer, highlighting the use of indirect evidence to draw conclusions about a related but unmeasured case.",
    ],
    2: [
        "The Quebec Bridge disaster highlights the limitations of engineering practices that relied on informal 'rules of thumb' before formal guidelines were developed. This suggests that engineers used such rules because rigorous analytical methods or technologies were inadequate at the time. Thus, the correct inference is (C), indicating that reliance on less formalized methods was not necessarily negligent but instead a product of limited engineering resources and analysis available before the incident reformed engineering practices.",
        "The collapse of the Quebec Bridge in 1907 revealed a significant reliance on informal engineering methods. This event, followed by a shift in engineering standards, suggests that engineers previously depended on rules of thumb, likely due to inadequate or less rigorous analytical methods. Therefore, (C) is the best answer, as it reflects the historical reliance on simplified methods that were later deemed insufficient, underscoring the limitations in engineering practices prior to the disaster.",
    ],
    3: [
        "The absence of a neutron star after the 1987 supernova challenges the assumption that such explosions always produce neutron stars. Supporting this argument requires evidence that neutron stars can arise from events other than supernovas, which would make the exception in 1987 plausible. The best answer is (E), as it introduces the idea that alternative causes for neutron star formation exist, reinforcing the claim that the supernova’s unique outcome does not invalidate the general theory but suggests other formation pathways.",
        "The missing neutron star following the 1987 supernova raises questions about the theory that supernovas always result in neutron stars. Evidence that other sources can create neutron stars, as in (E), strengthens the argument by challenging the notion that neutron stars must arise exclusively from supernovas, thereby allowing for variability in post-supernova remnants and supporting the anomalous outcome of the 1987 event.",
    ],
    4: [
        "The political scientist's argument asserts that democracy does not inherently promote freedom, citing examples of democratic oppression and despotisms that allow freedom. This reasoning confuses the concepts of necessary and sufficient conditions for freedom; just because democracy is not a guaranteed path to freedom, it does not mean it cannot promote it. Therefore, the best answer is (A), as the scientist mistakenly equates democracy’s lack of sufficiency for freedom with its complete inability to support freedom.",
        "The political scientist’s reasoning suggests that democracy does not guarantee freedom, using examples of democratic oppression and freedoms within certain despotisms. This logic conflates necessary and sufficient conditions, as democracy’s lack of absolute guarantee for freedom does not imply it is incapable of fostering it under the right conditions. The answer, therefore, is (A), indicating the flaw lies in confusing democracy’s potential for promoting freedom with its necessity or sufficiency in doing so.",
    ],
    5: [
        "The journalist critiques the practice of pharmaceutical companies setting high drug prices in wealthy nations and lower prices in poor ones, implying that equal access to healthcare should be the priority. This argument relies on a principle that those in need should receive priority consideration regardless of their country’s economic status. The answer is (A), as it aligns with the journalist’s perspective that moral obligations should focus on those in the greatest need, rather than differentiating based on wealth.",
        "The journalist critiques the pharmaceutical pricing model, arguing it is unjust for companies to charge higher prices in wealthier countries and lower prices in poorer ones, hinting at a moral imperative for equitable access. The argument hinges on the principle that those in greater need should receive more consideration, regardless of their country’s wealth. This aligns with (A), as it suggests that moral obligations should prioritize those in need rather than making distinctions based on economic status.",
    ],
}

# Constants
NUM_ROUNDS = 3
UI_OPTIONS = [0, 1]


# Classes
class SliderResponses:
    def __init__(self):
        self.relevance_preference = None
        self.validity_preference = None
        self.explainability_preference = None


class QuestionsAndAnswers:
    def __init__(self, question, answers_list):
        self.question = question
        self.question_key = None
        self.answers_without_o1 = answers_list[0]
        self.answers_with_o1 = answers_list[1]
        self.response_preference = None
        self.sliders = [SliderResponses(), SliderResponses()]
        self.question_identifier = None


# Helper Functions
def change_theme():
    previous_theme = st.session_state.themes["current_theme"]
    tdict = st.session_state.themes["light"] if st.session_state.themes["current_theme"] == "light" else \
    st.session_state.themes["dark"]
    for vkey, vval in tdict.items():
        if vkey.startswith("theme"):
            st._config.set_option(vkey, vval)
    st.session_state.themes["refreshed"] = False
    st.session_state.themes["current_theme"] = "light" if previous_theme == "dark" else "dark"
    st.session_state.current_theme = st.session_state.themes["current_theme"]


def theme_selection():
    btn_face = st.session_state.themes["light" if st.session_state.themes["current_theme"] == "light" else "dark"][
        "button_face"]
    st.button(btn_face, on_click=change_theme)
    if not st.session_state.themes["refreshed"]:
        st.session_state.themes["refreshed"] = True
        st.rerun()


def initialize_theme():
    current_theme = st.session_state.themes["current_theme"]
    theme_dict = st.session_state.themes[current_theme]
    for vkey, vval in theme_dict.items():
        if vkey.startswith("theme"):
            st._config.set_option(vkey, vval)


def apply_theme_to_question():
    current_theme = themes[st.session_state.current_theme]
    st.markdown(f"""
        <style>
            .my-container {{
                background-color: {current_theme["containerBackground"]};
                color: {current_theme["theme.textColor"]};
                border-radius: 10px;
                padding: 10px;
            }}
        </style>
    """, unsafe_allow_html=True)


def show_thinking_animation():
    st.write("Generating Output: Thinking...")
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.15)
        my_bar.progress(percent_complete + 1)
    st.write("Done!")


def submit_to_google_form(st, data):
    form_url = "https://docs.google.com/forms/d/e/1FAIpQLSfNfbHurMIpnRZE4YcPBTE27XUyMv7HJnW1JT-ikujAPIVp9g/formResponse"
    form_data = {
        'entry.117239958': data['round'],
        'entry.556492741': data['question'],
        'entry.1107608590': data['preference'],
        'entry.1327267302': data['relevance_preference'],
        'entry.1271752541': data['validity_preference'],
        'entry.1875781565': data['explainability_preference'],
    }
    try:
        response = requests.post(form_url, data=form_data)
        if response.status_code == 200:
            st.success("Response submitted successfully!")
        else:
            st.error(f"Error submitting response. Status code: {response.status_code}")
            save_response_locally(data)
    except Exception as e:
        st.error(f"Error submitting response: {e}")
        save_response_locally(data)


def save_response_locally(data):
    filename = 'responses.csv'
    exists = os.path.exists(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not exists:
            writer.writerow(
                ['Timestamp', 'Round', 'Question', 'Preference', 'Relevance Preference', 'Validity Preference',
                 'Explainability Preference'])
        writer.writerow(
            [datetime.now(), data['round'], data['question'], data['preference'], data['relevance_preference'],
             data['validity_preference'], data['explainability_preference']])


def display_button(question, question_key, round_num, q_index, answers):
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
        if st.session_state[f"thinking_output_{round_num}_{q_index}"] == 1 and question_key not in st.session_state[
            'thinking_shown']:
            show_thinking_animation()
            st.session_state['thinking_shown'][question_key] = True
        st.session_state[f"show_output1_{round_num}_{q_index}"] = True
        st.session_state[f"show_output2_button_{round_num}_{q_index}"] = True

    # Display Output 1 if generated
    if st.session_state[f"show_output1_{round_num}_{q_index}"]:
        st.write(f"**Output 1:** {answers[q_index][0]}")

        # Second button for Output 2
        if st.session_state[f"show_output2_button_{round_num}_{q_index}"]:
            if st.button(f"Generate 2nd Output",
                         key=f"output2_button_{round_num}_{q_index}"):
                if st.session_state[f"thinking_output_{round_num}_{q_index}"] == 2 and question_key not in \
                        st.session_state['thinking_shown']:
                    show_thinking_animation()
                    st.session_state['thinking_shown'][question_key] = True
                st.session_state[f"show_output2_{round_num}_{q_index}"] = True

    # Display Output 2 if generated
    if st.session_state[f"show_output2_{round_num}_{q_index}"]:
        st.write(f"**Output 2:** {answers[q_index][1]}")


def display_question(current_question):
    apply_theme_to_question()
    st.markdown(f'<div class="my-container">{current_question.question}</div>', unsafe_allow_html=True)


def display_sliders_collect_responses(current_question, q, round_num):
    st.write("Please provide your responses below:")

    current_question.response_preference = st.radio(
        f"Round {round_num} Question {q + 1} Preference",
        options=['1', '2'],
        index=None,
        key=f'response_preference_{round_num}_{q + 1}'
    )

    # Relevance Likert Scale (Horizontal layout)
    st.write("Relevance (1=Greater relevance in first response, 5=Greater relevance in second response)")
    current_question.sliders[q].relevance_preference = st.radio(
        "",
        options=[1, 2, 3, 4, 5],
        index=None,  # No pre-filled selection
        horizontal=True,  # Horizontal layout
        key=f'relevance_preference_{round_num}_{q + 1}'
    )

    # Validity Likert Scale (Horizontal layout)
    st.write("Validity (1=Greater validity in first response, 5=Greater validity in second response)")
    current_question.sliders[q].validity_preference = st.radio(
        "",
        options=[1, 2, 3, 4, 5],
        index=None,  # No pre-filled selection
        horizontal=True,  # Horizontal layout
        key=f'validity_preference_{round_num}_{q + 1}'
    )

    # Explainability Likert Scale (Horizontal layout)
    st.write("Explainability (1=Greater explainability in first response, 5=Greater explainability in second response)")
    current_question.sliders[q].explainability_preference = st.radio(
        "",
        options=[1, 2, 3, 4, 5],
        index=None,  # No pre-filled selection
        horizontal=True,  # Horizontal layout
        key=f'explainability_preference_{round_num}_{q + 1}'
    )
    st.button("Submit Response", key=f'submit_{round_num}_{q + 1}', on_click=submit_button_callback)


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


def submit_button_callback():
    q = st.session_state['current_question_within_round']
    round_num = st.session_state['current_round']
    current_question = st.session_state['current_question']

    # Validate responses before submitting
    if not validate_responses(round_num, q):
        st.warning("Please complete all responses before moving on to the next question.")
        return

    # Store responses if validation passes
    response_preference_key = f'response_preference_{round_num}_{q + 1}'
    current_question.response_preference = st.session_state.get(response_preference_key)

    relevance_preference_key = f'relevance_preference_{round_num}_{q + 1}'
    current_question.sliders[q].relevance_preference = st.session_state.get(relevance_preference_key)

    validity_preference_key = f'validity_preference_{round_num}_{q + 1}'
    current_question.sliders[q].validity_preference = st.session_state.get(validity_preference_key)

    explainability_preference_key = f'explainability_preference_{round_num}_{q + 1}'
    current_question.sliders[q].explainability_preference = st.session_state.get(explainability_preference_key)

    # Prepare response data for submission
    response_data = {
        'round': round_num,
        'question': q + 1,
        'preference': current_question.response_preference,
        'relevance_preference': current_question.sliders[q].relevance_preference,
        'validity_preference': current_question.sliders[q].validity_preference,
        'explainability_preference': current_question.sliders[q].explainability_preference
    }

    submit_to_google_form(st, response_data)
    st.session_state['responses'].append(response_data)

    # Transition to the next question or round
    if q == 1:
        st.session_state['current_round'] += 1
        st.session_state['current_question_within_round'] = 0
    else:
        st.session_state['current_question_within_round'] = 1

    st.session_state.placeholder_feedback.empty()
    st.success("Response submitted successfully. Moving to the next question.")


def start_questioning():
    if st.session_state['survey_started']:
        round_num = st.session_state['current_round']
        q = st.session_state['current_question_within_round']
        with_or_without_o1 = st.session_state['selected_ui']

        st.markdown(f"### Round {round_num}")
        start_index = (round_num - 1) * 2
        q_index = start_index + q

        # Use st.session_state['questions_and_answers'] instead of questions_and_answers
        if q_index < len(st.session_state['questions_and_answers']):
            current_question = st.session_state['remaining_questions'][q_index]
            question_key = f"round_{round_num}_q_{q}_{'with' if with_or_without_o1 else 'without'}_o1"
            current_question.question_key = question_key

            st.markdown(f"#### Question {q + 1}")
            display_question(current_question)
            display_button(current_question, question_key, round_num, q_index, answers)

            # Prevent sliders and next question from appearing until both outputs are shown
            if (st.session_state[f"show_output1_{round_num}_{q_index}"] and
                    st.session_state[f"show_output2_{round_num}_{q_index}"]):

                st.session_state.placeholder_feedback = st.empty()
                with st.session_state.placeholder_feedback.container():
                    display_sliders_collect_responses(current_question, q, round_num)
            else:
                st.warning("Please generate both outputs before proceeding.")


def survey_started_callback():
    st.session_state.survey_started = True


def intro_statement():
    st.header('CS 197 Project :computer:', divider='blue')
    st.subheader(':green[Introduction]')
    st.write(
        "This study explores whether user perception of AI responses changes when responses include language suggesting that the AI 'thought' about the answer. Please read both AI responses and answer the questions accordingly. :sunglasses::sunglasses:")

    theme_selection()

    if not st.session_state['survey_started']:
        st.button('Ready to start?', on_click=survey_started_callback)
    else:
        st.subheader(":red[Welcome to the Research Study]")
        st.write(f"You will be presented with {NUM_ROUNDS} rounds of questions.")
        st.write("Each round will show you 2 different questions with corresponding answers.")

        start_questioning()

        if st.session_state['current_round'] > NUM_ROUNDS:
            st.success("Thank you for participating in the study!")
            st.write("You can now close this tab.")


def main():
    st.set_page_config(page_title="O1 Study", page_icon="🎨")

    # Initialize session states
    if "themes" not in st.session_state:
        st.session_state.themes = themes

    if "current_theme" not in st.session_state:
        st.session_state.current_theme = st.session_state.themes["current_theme"]

    initialize_theme()

    # Initialize the questions_and_answers list before using it
    if 'questions_and_answers' not in st.session_state:
        questions_and_answers = []
        for i, question_text in enumerate(questions):
            question_and_answer = QuestionsAndAnswers(question_text, answers[i])
            questions_and_answers.append(question_and_answer)
        st.session_state['questions_and_answers'] = questions_and_answers

    session_state_vars = {
        'preliminaries_done': False,
        'survey_started': False,
        'thinking_shown': {},
        'remaining_questions': random.sample(st.session_state['questions_and_answers'],
                                             len(st.session_state['questions_and_answers'])),
        'current_round': 1,
        'current_question_within_round': 0,
        'selected_ui': random.choice([0, 1]),
        'responses': [],
        'show_content': True,
        'stage': 0
    }

    for var, value in session_state_vars.items():
        if var not in st.session_state:
            st.session_state[var] = value

    if 'current_question' not in st.session_state:
        st.session_state['current_question'] = st.session_state['remaining_questions'][0]

    if 'first_answer_ui_chosen' not in st.session_state:
        st.session_state['first_answer_ui_chosen'] = True

    intro_statement()


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


def display_selected_ui(current_question, question_key):
    if not st.session_state['first_answer_ui_chosen']:
        pick_ui()

    if st.session_state['first_answer_ui_chosen']:
        st.session_state['first_answer_ui_chosen'] = False


if __name__ == '__main__':
    main()
