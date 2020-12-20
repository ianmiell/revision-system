#!/usr/bin/env python3
import os
import random
import rsdb
import shared


# Q&A - looks through learning folder for asciidoc files
def run_qanda():
	global DEBUG
	global ROOT_DIR
	page(msg='Doing Q&A, ret to continue')
	files = set()
	debug(days)
	if nday_scan_days != -1:
		cmd = '''git whatchanged --since="''' + str(nday_scan_days) + ''' days ago" --pretty=format:'' ''' + ROOT_DIR + '''/learning | grep -v '^$' | sort -u | grep -v README | grep asciidoc'''
		debug(cmd)
		new_files = set(os.popen(cmd).read().rstrip("\n").split('\n'))
		files = files.union(new_files)
	else:
		for day in days:
			cmd = '''git whatchanged --since="''' + day + ''' days ago" --until="$[''' + day + '''-1] days ago" --name-only --pretty=format:'' ''' + ROOT_DIR + '''/learning | grep -v '^$' | sort -u | grep -v README | grep asciidoc'''
			debug(cmd)
			new_files = set(os.popen(cmd).read().rstrip("\n").split('\n'))
			if new_files == set(['']):
				continue
			files = files.union(new_files)
		# TODO: also have a 'check knowledge of q: questions'
	debug(files)
	if files == set():
		# Catch files older than last day BEGIN
		cmd = '''git whatchanged --before="''' + days[-1] + ''' days ago" --name-only --pretty=format:'' ''' + ROOT_DIR + '''/learning | grep -v '^$' | sort -u | grep -v README | grep asciidoc'''
		debug(cmd)
		new_files = set(os.popen(cmd).read().rstrip("\n").split('\n'))
		if new_files != set(['']):
			files = files.union(new_files)
		# Catch files older than last day DONE
	debug("Files found: " + str(files))
	# Do the questions
	questions_from_files(files)
	print('============================\nDone doing qanda\n============================')


def questions_from_files(files, image_files):
	global ROOT_FILE
	global OS_TYPE
	global DEBUG
	questions       = []
	answers         = []
	qanda_files     = []
	for f in files:
		debug('Looking at: ' + f)
		question = ''
		answer = ''
		cmd = "cat " + ROOT_DIR + "/" + f + " 2> /dev/null"
		debug(cmd)
		changes = os.popen(cmd).read().rstrip("\n").split('\n')
		if changes == ['']:
			debug('No content in: ' + f)
			continue
		for change in changes:
			if change[:2] == 'Q:':
				# Starting a question - clean up any answer and start new question
				question = change[2:].strip()
				if answer != '':
					answers.append(answer)
				answer = ''
			elif change[:2] == 'q:':
				# A 'done' question - ignore this and following answer
				question = ''
				if answer != '':
					answers.append(answer)
				answer = ''
			elif change[:2] == 'A:':
				# If there's an active question, add it
				if question != '':
					questions.append(question)
					question = ''
					qanda_files.append(f)
					answer = change[2:].strip()
			elif question != '':
				# If in a question, add to it
				question += '\r\n' + change.strip()
			elif answer != '':
				# If in an answer, add to it
				answer += '\r\n' + change.strip()
		if answer != '':
			answers.append(answer)
		if len(questions) != len(answers):
			print('Problem with file: ' + f)
			assert False
	assert len(questions) == len(answers) == len(qanda_files)
	# zip questions and answers together and run through.
	questions_and_answers = zip(questions,answers,qanda_files)
	num_items = len(questions)
	for item in questions_and_answers:
		print('QUESTION (' + str(num_items) + ' left) from file: ' + item[2])
		print('Q: ' + item[0], end='')
		page(msg='')
		print('A: ' + item[1], end='')
		page(msg='')
		ask_revise(item)
		num_items -= 1
	image_files = list(image_files)
	num_items = len(image_files)
	while num_items > 0:
		item_no = int(random.random() * num_items)
		item = image_files[item_no]
		print('Image file: ' + item)
		if OS_TYPE == 'Darwin':
			cmd = '''open ''' + item
		os.popen(cmd)
		page(msg='ret to continue')
		image_files.remove(item)
		num_items = len(image_files)
