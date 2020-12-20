#!/usr/bin/env python3
import os
import random
import pick
import rsdb
import shared
import tag


# Q&A - looks through learning folder for asciidoc files
def run_qanda():
	days = get_days()
	shared.page(msg='Doing Q&A, hit Return to continue')

	question_ids        = set()
	tagged_question_ids = set()
	tag_ids             = []

	# Choose tags, get related questions
	tag_tuples          = tag.choose_tags()
	tagged_question_ids = get_tagged_questions(tag_tuples)

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
		question, answer, question_status = get_question(question_id)
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
		picked_list = pick.pick(options, title, multi_select=True, indicator='=>', options_map_func=shared.get_option_description)
		for picked in picked_list:
			print(picked)
			action = picked[0].get('action')
			if action == 'right':
				rsdb.insert_answer(question_id, 'R')
			else:
				rsdb.insert_answer(question_id, 'W')
			if action == 'inactive':
				rsdb.update_question_status(question_id, 'I')
			if action == 'active':
				rsdb.update_question_status(question_id, 'A')
			# Revise over-rides inactive
			if action == 'revise':
				rsdb.update_question_status(question_id, 'R')


def review_questions():
	# Choose tags
	tag_tuples = tag.choose_tags()
	tagged_question_ids = get_tagged_questions(tag_tuples)
	for question_id in tagged_question_ids:
		question, answer, question_status = get_question(question_id)
		status_description = get_status(question_status)
		title = 'Question:\n\n\t' + question + '\n\n\t' + answer + '\n\nCurrent status: ' + status_description + '\n\nENTER to choose, UP/DOWN to move'
		options = [
			{'action': 'do_nothing', 'description': 'Do nothing'},
			{'action': 'inactive', 'description': 'Do not ask again'},
		]
		if question_status == 'R':
			options.append({'action': 'active',   'description': 'Make question active'})
			options.append({'action': 'inactive', 'description': 'Make question inactive'})
		elif question_status == 'A':
			options.append({'action': 'inactive', 'description': 'Make question inactive'})
			options.append({'action': 'revise',   'description': 'Revise (ask me every time)'})
		elif question_status == 'I':
			options.append({'action': 'active',   'description': 'Make question active'})
			options.append({'action': 'revise',   'description': 'Revise (ask me every time)'})
		res = pick.pick(options, title, multi_select=False, indicator='=>', options_map_func=shared.get_option_description)


def get_question(question_id):
	question_res    = rsdb.get_question(question_id)
	question        = question_res[1]
	answer          = question_res[2]
	question_status = question_res[3]
	return question, answer, question_status


def get_days():
	# Prime numbers
	days=[1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
	# From 'How to learn'
	#days=[1, 2, 3, 5, 7, 14, 21, 28, 42, 56, 70, 84, 105, 126, 147, 168, 189, 219, 249, 279, 309, 339, 369]
	# More 'spaced out'
	#days=[1, 2, 4, 8, 12, 16, 24, 40, 60, 80, 100, 120, 150, 200]
	return days


def get_status(status):
	if status == 'R':
		return 'Revise'
	if status == 'I':
		return 'Inactive'
	if status == 'A':
		return 'Active'


def get_tagged_questions(tag_tuples):
	tag_ids = []
	for tag_tuple in tag_tuples:
		tag_ids.append(tag_tuple[1])
	# Get related questions
	tagged_question_ids = rsdb.get_related_questions(tag_ids)
	assert isinstance(tagged_question_ids, list)
	return tagged_question_ids


if __name__ == '__main__':
	shared.page('test run qanda')
	run_qanda()
	shared.page('review questions')
	review_questions()
