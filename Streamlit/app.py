import streamlit as st

import time

import requests



from questions import *
import random

# Define study constants

NUM_ROUNDS = 3






def submit_to_google_form(data):

	"""Submit response data to Google Form."""

	# Google Form URL (formResponse endpoint)

	form_url = "https://docs.google.com/forms/d/e/1FAIpQLSdVo6Tw-ahAB3sSPKYH6u75LKmnXgt-3neDDorqM-DIzcBCBw/formResponse"



	# Form data with entry IDs

	form_data = {

		'entry.132741864': data['round'],            # Round number field

		'entry.1766629492': data['question'],         # Question number field

		'entry.1357460269': data['preference'],       # Preference field

		'entry.312523467': data['relevance_1'],       # Answer 1 Relevance field

		'entry.541926730': data['relevance_2'],       # Answer 2 Relevance field

		'entry.1624496186': data['validity_1'],       # Answer 1 Validity field

		'entry.2065218302': data['validity_2'],       # Answer 2 Validity field

		'entry.652819736': data['explainability_1'],  # Answer 1 Explainability field

		'entry.1063036354': data['explainability_2']  # Answer 2 Explainability field

	}



	headers = {

		'Referer': form_url,

		'User-Agent': 'Mozilla/5.0'

	}



	try:

		response = requests.post(

			form_url,

			data=form_data,

			headers=headers

		)



		if response.status_code == 200:

			st.success("Response submitted successfully!")

		else:

			st.error(f"Error submitting response. Status code: {response.status_code}")

			st.info("Recording response locally...")

			save_response_locally(data)



	except Exception as e:

		st.error(f"Error submitting response: {e}")

		st.info("Recording response locally...")

		save_response_locally(data)







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
	preference = st.radio(f"Round {round_num} Question {q+1} Preference", options=['1', '2'], key=f'preference_{round_num}_{q+1}')

	# Your existing sliders for relevance, validity, and explainability...
	relevance_1 = st.slider(f"GPT 4o Output 1 Relevance (1=Not relevant, 5=Highly relevant)", min_value=1, max_value=5, key=f'relevance1_{round_num}_{q+1}')
	relevance_2 = st.slider(f"GPT 4o Output 2 Relevance (1=Not relevant, 5=Highly relevant)", min_value=1, max_value=5, key=f'relevance2_{round_num}_{q+1}')
	validity_1 = st.slider(f"GPT 4o Output 1 Validity (1=Not valid, 5=Highly valid)", min_value=1, max_value=5, key=f'validity1_{round_num}_{q+1}')
	validity_2 = st.slider(f"GPT 4o Output 2 Validity (1=Not valid, 5=Highly valid)", min_value=1, max_value=5, key=f'validity2_{round_num}_{q+1}')
	explainability_1 = st.slider(f"GPT 4o Output 1 Explainability (1=Not clear, 5=Very clear)", min_value=1, max_value=5, key=f'explain1_{round_num}_{q+1}')
	explainability_2 = st.slider(f"GPT 4o Output 2 Explainability (1=Not clear, 5=Very clear)", min_value=1, max_value=5, key=f'explain2_{round_num}_{q+1}')

	if st.button('Submit Response', key=f'submit_{round_num}_{q+1}'):
		response_data = {
						'round': round_num,
						'question': q + 1,
						'preference': preference,
						'relevance_1': relevance_1,
						'relevance_2': relevance_2,
						'validity_1': validity_1,
						'validity_2': validity_2,
						'explainability_1': explainability_1,
						'explainability_2': explainability_2
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
			#st.session_state['refresh_key'] = not st.session_state['refresh_key']

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
		
		if q_index < len(questions):  # Ensure within bounds
			
			question_key = f"round_{round_num}_q_{q}"



			st.markdown(f"#### Question {q+1}")

			st.write(st.session_state['remaining_questions'][q_index])



			# Display GPT 4o Output 1

			with st.expander("Click to see GPT 4o Output 1"):
				st.write(answers[q_index][0])



			# Show thinking animation only once per question
			if question_key not in st.session_state['thinking_shown']:

				show_thinking_animation()

				st.session_state['thinking_shown'][question_key] = True



			# Display GPT 4o Output 2

			with st.expander("Click to see GPT 4o Output 2"):

				st.write(answers[q_index][1])


			display_sliders_collect_responses(q, round_num)


def intro_statement():

	
	st.header('CS 197 Project :computer:', divider='blue')



	st.subheader(':green[Introduction]')

	st.write("This study explores whether user perception of AI responses changes when responses include language suggesting that the AI 'thought' about the answer. Please read both AI responses and answer the questions accordingly. :sunglasses::sunglasses:")


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
		st.session_state['remaining_questions'] = random.sample(questions, len(questions))

	if 'current_round' not in st.session_state:

		st.session_state['current_round'] = 1

	if 'current_question' not in st.session_state:

		st.session_state['current_question'] = 0

	if 'responses' not in st.session_state:

		st.session_state['responses'] = []


	intro_statement()




if __name__ == '__main__':

	main()