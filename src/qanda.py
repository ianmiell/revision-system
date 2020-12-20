#!/usr/bin/env python3
import os
import random
import rsdb
import shared




# Prime numbers
days=['1','2','3','5','7','11','13','17','19','23','29','31','37','41','43','47','53','59','61','67','71','73','79','83','89','97','101']
# From 'How to learn'
#days=['1','2','3','5','7','14','21','28','42','56','70','84','105','126','147','168','189','219','249','279','309','339','369']
# More 'spaced out'
#days=['1','2','4','8','12','16','24','40','60','80','100','120','150','200']

# Q&A - looks through learning folder for asciidoc files
def run_qanda():
	global ROOT_DIR
	page(msg='Doing Q&A, hit Return to continue')
	# Choose tags
	TODO
	# Get days
	for day in days:
		# Find all questions that are linked to those tags
		question_ids = get_related_questions(tag_ids)
		# Of those questions, ask any that are 'day' days old OR have not been asked enough.
		for question_id in question_ids:
			# Is q 'n' days old? If not,
			# How many times has it been asked?
			# If

	TODO: end up with a list of question_ids

	# Do the questions
	ask_questions(question_ids)
	print('============================\nDone doing qanda\n============================')

