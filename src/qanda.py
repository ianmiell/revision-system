#!/usr/bin/env python3
import os
import random
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
			pass
			# TODO: if question is in 'R'evise mode, always ask it
			else:
				# TODO: If not, how many times has it been asked? If less than the number of times, then ask it.
				pass
	# Ask the questions
	ask_questions(list(question_ids))

def ask_questions(question_ids):
	assert isinstance(question_ids, list)
	for question_id in question_ids:
		pass
		# Retrieve question
		# Ask question
		# Give answer
		# Give options to:
			# Mark q as correct/failed
				# Pass question_id, result=R/W to insert into answer table
			# Change question status:
				# Never ask again (ie, make inactive)?
					# Update question if inactive
				# Toggle revise mode for question
					# Update question if changing mode
