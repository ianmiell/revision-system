#!/usr/bin/env python3
import os
import random
import pick
import rsdb
import shared
import tag

# Prime numbers
days=[1,2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]
# From 'How to learn'
#days=[1,2,3,5,7,14,21,28,42,56,70,84,105,126,147,168,189,219,249,279,309,339,369]
# More 'spaced out'
#days=[1,2,4,8,12,16,24,40,60,80,100,120,150,200]

# Q&A - looks through learning folder for asciidoc files
def run_qanda():
	shared.page(msg='Doing Q&A, hit Return to continue')

	question_ids        = set()
	tagged_question_ids = set()
	tag_ids             = []

	# Choose tags
	tag_tuples = tag.choose_tags()
	for tag_tuple in tag_tuples:
		print(tag_tuple)
		tag_ids.append(tag_tuple[1])
		print(tag_ids)
	# Get related questions
	tagged_question_ids = rsdb.get_related_questions(tag_ids)
	assert isinstance(tagged_question_ids, list)
	# Get days
	for question_id in tagged_question_ids:
		# How many days old is the question?
		age = rsdb.get_question_age(question_id)
		assert isinstance(age, int)
		# If q is 'n' days old, add it.
		if age in days:
			question_ids.add(question_id)
		else:
			# If question is in 'R'evise mode, always ask it
			question_status = rsdb.get_question_state(question_id)
			assert isinstance(question_status, string)
			if question_status == 'R':
				question_ids.add(question_id)
			else:
				# If not, how many times has it been asked? If less than the number of days before that it should have been asked (the index), then ask it.
				times_asked = rsdb.get_times_asked(question_id)
				assert isinstance(times_asked, int)
				if times_asked < days.index(age)+1:
					question_ids.add(question_id)
	# Ask the questions
	ask_questions(list(question_ids))

def ask_questions(question_ids):
	assert isinstance(question_ids, list)
	num_questions           = len(question_ids)
	num_questions_remaining = num_questions
	for question_id in question_ids:
		# Retrieve question
		question_res = rsdb.get_question(question_id)
		question        = question_res[1]
		answer          = question_res[2]
		question_status = question_res[3]
		# Ask question
		shared.page('Q: ' + question)
		# Give answer
		shared.page('A: ' + answer)
		title = 'Your answer to question:\n\n\t' + question + '\n\nSPACE to confirm, ENTER to continue, UP/DOWN to move'
		options = [
			{'action': 'right',    'description': 'I got that right'},
			{'action': 'inactive', 'description': 'Do not ask again'},
		]
		if question_status == 'R':
			options.append({'action': 'active',   'description': 'Take out of revise mode'})
		else:
			options.append({'action': 'revise',   'description': 'Revise (ask me every time)'})
		def get_option_description(option):
			return option.get('description')
		res = pick.pick(options, title, multi_select=True, indicator='=>', options_map_func=get_option_description)
		for res in res:
			if res.get('action') == 'right':
				rsdb.insert_answer(question_id, 'R')
			else:
				rsdb.insert_answer(question_id, 'W')
			if res.get('action') == 'inactive':
				rsdb.update_question_status(question_id, 'I')
			if res.get('action') == 'active':
				rsdb.update_question_status(question_id, 'A')
			if res.get('action') == 'revise':
				rsdb.update_question_status(question_id, 'R')

if __name__ == '__main__':
	ask_questions([1])
