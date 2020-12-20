#!/usr/bin/env python3
import pick
import sys
import time
import qanda
import tag
import question
import shared

def main():
	while True:
		options = [
			{'action': 'qanda',        'description': 'Do Q and A'},
			{'action': 'revise',       'description': 'Revision questions'},
			{'action': 'add_question', 'description': 'Add a question'},
			{'action': 'add_tag',      'description': 'Add a tag'},
			{'action': 'bulk_insert',  'description': 'Bulk insert question'},
			{'action': 'review',       'description': 'Review questions'},
			{'action': 'quit',         'description': 'Save state and quit'}
		]
		res = pick.pick(options, title='Choose: ', options_map_func=shared.get_option_description, min_selection_count=1)
		action = res[0].get('action')
		do_qanda     = False
		revise       = False
		add_question = False
		add_tag      = False
		bulk_insert  = False
		review       = False
		if action == 'qanda':
			do_qanda = True
		elif action == 'revise':
			revise = True
		elif action == 'add_question':
			add_question = True
		elif action == 'add_tag':
			add_tag = True
		elif action == 'bulk_insert':
			bulk_insert = True
		elif action == 'review':
			review = True
		elif action == 'quit':
			sys.exit()
		if revise:
			run_revise()
		if do_qanda:
			qanda.run_qanda()
		if add_question:
			question.add_question()
		if bulk_insert:
			question.bulk_insert()
		if add_tag:
			tag.add_tag()
		if review:
			qanda.review_questions()
		print('Completed cycle, starting again - remember to save state at the end of the session.')
		time.sleep(3)


if __name__ == '__main__':
	if sys.version_info.major == 2:
		print('Must be python3')
		sys.exit(1)
	main()
