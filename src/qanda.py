#-*-coding:utf-8-*-
import os
import random
import sys
import pick
import time
import rsdb
import shared
import tag
import question
import datetime


# Q&A - looks through learning folder for asciidoc files
def run_qanda(nosort=False, lastminute=False):
	shared.clear_screen()

	days                       = get_days()
	question_ids               = set()
	tagged_question_ids        = set()
	tag_ids                    = []
	already_asked_today_count  = 0
	deferred_questions_count   = 0
	inactive_questions_count   = 0
	not_considered_today_count = 0

	# Choose tags, get related questions
	result, tag_ids             = question.choose_tags()
	if not result:
		return False
	tagged_question_ids = get_tagged_questions(tag_ids)

	for question_id in tagged_question_ids:
		# How many days old is the question?
		age = rsdb.get_question_age(question_id)
		assert isinstance(age, int)
		question_status = rsdb.get_question_status(question_id)
		assert isinstance(question_status, str)
		# If question is in 'R'evise mode, always ask it
		if question_status == 'R':
			question_ids.add(question_id)
		elif question_status == 'I':
			# If question is inactive, don't include it.
			inactive_questions_count += 1
			continue
		ask_after = rsdb.get_ask_after(question_id)
		if ask_after is not None and ask_after >= datetime.datetime.today().strftime('%Y-%m-%d'):
			deferred_questions_count += 1
			continue
		# If it has already been asked today, do not ask again
		if rsdb.asked_today(question_id):
			already_asked_today_count += 1
			continue
		# If q is 'n' days old, add it.
		if age in days:
			question_ids.add(question_id)
		else:
			# If not, how many times has it been asked? If less than the number of days before that it should have been asked (the index), then ask it.
			times_asked = rsdb.get_times_asked(question_id)
			assert isinstance(times_asked, int)
			# Find number of days in list that is less than age of question, ie how many times this should have been asked.
			count = 0
			for day in days:
				count += 1
				if day >= age:
					break
			day = None
			# If this hasn't been asked enough, ask it.
			if times_asked < count:
				question_ids.add(question_id)
			else:
				not_considered_today_count += 1
			count, times_asked, question_status = None, None, None
	tag_ids, tagged_question_ids = None, None

	# For all questions, divide them into groups:
	#       - questions that have never been asked
	#       - questions that have been answered but always wrongly
	#       - questions that were last answered wrongly
	#       - questions that have been answered wrongly previously
	#       - questions that have always been answered correctly
	# Then shuffle within these groups.
	asked_but_always_answered_wrongly  = list()
	never_asked                        = list()
	last_answered_wrongly              = list()
	previously_answered_wrongly        = list()
	asked_and_always_right             = list()
	for question_id in question_ids:
		_, _, _, answers = rsdb.get_question_history(question_id)
		results = list()
		for answer in answers:
			results.append(answer[1])
		if not results:
			never_asked.append(question_id)
		# Always wrong
		elif results[0] == 'W' and len(set(results)) == 1:
			asked_but_always_answered_wrongly.append(question_id)
		elif results[0] == 'R' and len(set(results)) == 1:
			asked_and_always_right.append(question_id)
		elif results[-1] == 'W':
			last_answered_wrongly.append(question_id)
		elif any('W'):
			previously_answered_wrongly.append(question_id)
		# Some other category?
		else:
			print('Un-captured quesiton history category - BUG')
			print(results)
			sys.exit(1)
	if nosort:
		random.shuffle(never_asked)
		random.shuffle(asked_but_always_answered_wrongly)
		random.shuffle(last_answered_wrongly)
		random.shuffle(previously_answered_wrongly)
		random.shuffle(asked_and_always_right)
	question_ids = never_asked + asked_but_always_answered_wrongly + last_answered_wrongly + previously_answered_wrongly + asked_and_always_right
	print('Questions to be asked:')
	print('There are ' + str(len(never_asked)) + ' questions that have never been asked')
	print('There are ' + str(len(asked_but_always_answered_wrongly)) + ' questions that have been asked but have only been answered wrongly')
	print('There are ' + str(len(last_answered_wrongly)) + ' questions that were last answered wrongly')
	print('There are ' + str(len(previously_answered_wrongly)) + ' questions that have been previously answered wrongly')
	print('There are ' + str(len(asked_and_always_right)) + ' questions that have always been answered correctly')
	print('')
	print('Other questions that will not be asked:')
	print('There are ' + str(already_asked_today_count) + ' questions that have already been answered today')
	print('There are ' + str(deferred_questions_count) + ' deferred questions')
	print('There are ' + str(not_considered_today_count) + ' questions that are not being considered today')
	print('There are ' + str(inactive_questions_count) + ' inactive questions')
	print('')
	shared.page()
	if lastminute:
	    # Show the questions
		show_questions(list(question_ids))
	else:
	    # Ask the questions
		ask_questions(list(question_ids))
	question_ids = None
	return True


def run_revise():
	shared.clear_screen()
	question_ids        = set()
	tagged_question_ids = set()
	tag_ids             = []

	# Choose tags, get related questions
	result, tag_ids             = question.choose_tags()
	if not result:
		return False
	tagged_question_ids = get_tagged_questions(tag_ids)
	for question_id in tagged_question_ids:
		question_status = rsdb.get_question_status(question_id)
		if question_status == 'R':
			question_ids.add(question_id)
	tag_ids, tagged_question_ids = None, None
	# Ask the questions
	ask_questions(list(question_ids))
	question_ids = None
	return True


def show_questions(question_ids):
	assert isinstance(question_ids, list)
	num_questions           = len(question_ids)
	num_questions_remaining = num_questions
	num_questions_asked     = 0
	for question_id in question_ids:
		num_questions_remaining -= 1
		num_questions_asked     += 1
		question_string, answer, question_status = get_question(question_id)
		# Ask question
		shared.clear_screen()
		shared.hash_image(question_string)
		shared.page('\nQuestion ' + str(num_questions_asked) + ' of ' + str(num_questions) + '\n\nQuestion:\n' + shared.hash_color_string(question_string) + '\n\nAnswer:\n' + shared.hash_color_string(answer))


def ask_questions(question_ids):
	assert isinstance(question_ids, list)
	num_questions           = len(question_ids)
	num_questions_remaining = num_questions
	num_questions_asked     = 0
	for question_id in question_ids:
		num_questions_remaining -= 1
		num_questions_asked     += 1
		question_string, answer, question_status = get_question(question_id)
		# Ask question
		shared.clear_screen()
		shared.hash_image(question_string)
		shared.page('\nQuestion ' + str(num_questions_asked) + ' of ' + str(num_questions) + '\n\nQuestion:\n' + shared.hash_color_string(question_string))
		# Give answer
		shared.page('\nAnswer:\n' + shared.hash_color_string(answer))
		title = get_question_history(question_id) + '\nSPACE to confirm, ENTER to continue, UP/DOWN to move\n'
		options = [
			{'action': 'right',    'description': 'I got that right'},
			{'action': 'wrong',    'description': 'I got that wrong'},
			{'action': 'edit',     'description': 'Edit question'},
			{'action': 'delete',   'description': 'Permanently delete question'},
			{'action': 'done',     'description': 'Return to main menu'},
			{'action': 'quit',     'description': 'Quit and save state'},
			{'action': 'new',      'description': 'Set question as newly-added'},
			{'action': 'nothing',  'description': 'Do nothing'},
		]
		if question_status == 'R':
			options.append({'action': 'active',   'description': 'Take out of revise mode'})
			options.append({'action': 'inactive', 'description': 'Do not ask again for n days'})
		elif question_status == 'A':
			options.append({'action': 'revise',   'description': 'Revise (ask me every time)'})
			options.append({'action': 'inactive', 'description': 'Do not ask again for n days'})
		elif question_status == 'I':
			options.append({'action': 'active',   'description': 'Take out of revise mode'})
			options.append({'action': 'revise',   'description': 'Revise (ask me every time)'})
		while True:
			picked_list = pick.pick(options, title, multi_select=True, indicator='x', min_selection_count=1, options_map_func=shared.get_option_description)
			active   = False
			delete   = False
			done     = False
			edit     = False
			inactive = False
			new      = False
			nothing  = False
			quit     = False
			revise   = False
			right    = False
			wrong    = False
			# Gather choices
			for picked in picked_list:
				action = picked[0].get('action')
				if action == 'active':
					active   = True
				if action == 'delete':
					delete   = True
				if action == 'done':
					done     = True
				if action == 'edit':
					edit     = True
				if action == 'inactive':
					inactive = True
				if action == 'new':
					new = True
				if action == 'nothing':
					nothing  = True
				if action == 'quit':
					quit     = True
				if action == 'revise':
					revise   = True
				if action == 'right':
					right    = True
				if action == 'wrong':
					wrong    = True
			# Checks
			if right and wrong:
				print('Cannot be right and wrong!')
				time.sleep(2)
				continue
			if not right and not wrong and not delete and not done and not edit and not inactive and not nothing and not quit and not revise and not new:
				print('Must pick one!')
				time.sleep(2)
				continue
			if (right or wrong or active or inactive or revise or edit or new) and (nothing or delete):
				print('Cannot do nothing or delete, and be right, wrong, active, or inactive!')
				time.sleep(2)
				continue
			if (active and inactive) or (inactive and revise) or (active and revise):
				print('Cannot be multiple states (should not get here)!')
				time.sleep(2)
				continue
			# Handle choices in correct order
			if wrong:
				rsdb.insert_answer(question_id, 'W')
			elif right:
				rsdb.insert_answer(question_id, 'R')
			if inactive:
				make_inactive(question_id, question_string, answer)
			if active:
				rsdb.update_question_status(question_id, 'A')
			if revise:
				rsdb.update_question_status(question_id, 'R')
			if edit:
				edit_question(question_id, question_string, answer)
			if delete:
				rsdb.delete_question(question_id)
			if new:
				rsdb.update_question_new(question_id)
			if done:
				return
			if quit:
				sys.exit(0)
			if nothing:
				break
			break


def make_inactive(question_id, question_string, answer):
	shared.clear_screen()
	print('\nQuestion was: \n\n\t' + shared.hash_color_string(question_string))
	print('\nAnswer was: \n\n\t' + shared.hash_color_string(answer))
	print('\nMake question inactive for how many days (0 == forever, no number == cancel):\n')
	try:
		days = int(input().strip())
		if days == 0:
			rsdb.update_question_status(question_id, 'I')
			print('\nNo number given, cancelling\n')
		else:
			rsdb.update_question_ask_after(question_id, days)
			print('\nQuestion inactive for ' + str(days) + ' days\n')
		time.sleep(2)
		shared.clear_screen()
	except ValueError:
		print('\nNo number given, cancelling\n')
		time.sleep(2)
		shared.clear_screen()


def edit_question(question_id, question, answer):
	assert isinstance(question_id, int)
	assert isinstance(question, str)
	assert isinstance(answer, str)
	shared.clear_screen()
	print('Question was: \n\n\t' + shared.hash_color_string(question))
	print('\nAnswer was: \n\n\t' + shared.hash_color_string(answer))
	print('\nUpdate question as (blank for leave as-is):\n')
	new_question = shared.input_paragraph().strip()
	print('\nUpdate answer as (blank for leave as-is):\n')
	new_answer = shared.input_paragraph().strip()
	if new_question != '':
		rsdb.update_question(question_id, new_question)
		print('\nQuestion updated\n')
	if new_answer != '':
		rsdb.update_answer(question_id, new_answer)
		print('\nAnswer updated\n')
	time.sleep(2)
	shared.clear_screen()


def review_questions():
	shared.clear_screen()
	# Choose tags
	result, tag_ids             = question.choose_tags()
	if not result:
		return False
	tagged_question_ids = get_tagged_questions(tag_ids)
	# Shuffle questions
	random.shuffle(tagged_question_ids)
	for question_id in tagged_question_ids:
		question_string, answer, question_status = get_question(question_id)
		status_description = get_status(question_status)
		title = 'Question:\n\n\t' + question_string + '\n\nAnswer:\n\n\t' + answer + '\n\nCurrent status: ' + status_description + '\n\nENTER to choose, UP/DOWN to move'
		options = [
			{'action': 'do_nothing', 'description': 'Do nothing'},
			{'action': 'inactive',   'description': 'Do not ask again for n days'},
			{'action': 'history',    'description': 'Show question history'},
			{'action': 'tag',        'description': 'Tag question'},
			{'action': 'finish',     'description': 'Finish review'},
			{'action': 'edit',       'description': 'Edit question'},
			{'action': 'new',        'description': 'Set question as newly-added'},
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
		while True:
			res = pick.pick(options, title, multi_select=False, indicator='=>', options_map_func=shared.get_option_description)
			action = res[0].get('action')
			if action == 'do_nothing':
				break
			elif action == 'edit':
				edit_question(question_id, question_string, answer)
			elif action == 'finish':
				return True
			elif action == 'inactive':
				make_inactive(question_id, question_string, answer)
				rsdb.update_question_status(question_id, 'I')
				break
			elif action == 'revise':
				rsdb.update_question_status(question_id, 'R')
				break
			elif action == 'tag':
				result, tag_ids = question.choose_tags()
				if not result:
					continue
				rsdb.add_question_tags(question_id, tag_ids)
				break
			elif action == 'history':
				shared.clear_screen()
				print(get_question_history(question_id))
				shared.page()
				continue
			elif action == 'new':
				rsdb.update_question_new(question_id)
				break
	return True


def get_question(question_id):
	question_res    = rsdb.get_question(question_id)
	question        = question_res[1].strip()
	answer          = question_res[2].strip()
	question_status = question_res[3].strip()
	return question, answer, question_status


def get_question_history(question_id):
	history_string = ''
	date_added, question, answer, answers = rsdb.get_question_history(question_id)
	history_string += '\nQuestion:\n' + question
	history_string += '\nAnswer:\n' + answer
	history_string += '\nQuestion added on: ' + date_added + '\n\n'
	if not answers:
		history_string += 'This question has not been answered yet.\n'
	for answer in answers:
		time   = answer[0]
		result = answer[1]
		if result == 'R':
			result = '✔'
		elif result == 'W':
			result = 'x'
		else:
			print('result was: ' + result + ', this is a bug')
			sys.exit(1)
		history_string += 'At ' + time + ' your answer was ' + result + '\n'
	return history_string


def get_days():
	# Prime numbers
	#days=[1, 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
	# From 'How to learn'
	days=[1, 2, 3, 5, 7, 14, 21, 28, 42, 56, 70, 84, 105, 126, 147, 168, 189, 219, 249, 279, 309, 339, 369]
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


def get_tagged_questions(tag_ids_set):
	assert isinstance(tag_ids_set, set)
	tag_ids_list = list(tag_ids_set)
	for tag_id in tag_ids_list:
		assert isinstance(tag_id, int)
	# Get related questions
	tagged_question_ids = rsdb.get_related_questions(tag_ids_list)
	assert isinstance(tagged_question_ids, list)
	return tagged_question_ids


if __name__ == '__main__':
	shared.page('test run qanda')
	run_qanda()
	shared.page('review questions')
	review_questions()
