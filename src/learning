#!/usr/bin/env python3
import os
import random
import platform
import sys
import pick


def page(msg='[Hit enter to continue]'):
	if msg != '':
		print(msg)
	if sys.version_info.major == 2:
		raw_input()
	else:
		input()


# ask user if they want to add the qanda to the REVISE file
def ask_revise(qanda, msg='Do you want to add this to the REVISE file?'):
	global ROOT_DIR
	if msg != '':
		print(msg)
	if sys.version_info.major == 2:
		resp = raw_input()
	else:
		resp = input()
	# TODO: get input, and then switch on it. Open the REVISE file and add to it (if it's not already there?).
	if resp in ['yes','y','Y','YES']:
		f=open(ROOT_DIR + "/learning/REVISE", "a+")
		f.write('\nQ: ' + qanda[0].strip())
		f.write('A: ' + qanda[1].strip() + '\n')
		f.close()


# Does questions in REVISE file always, until they are deleted
def run_revise(msg='Doing revise, hit return to continue'):
	global ROOT_DIR
	global DEBUG
	page(msg=msg)
	cmd = '''cat ''' + ROOT_DIR + '''/learning/REVISE'''
	debug(cmd)
	output = os.popen(cmd).read().rstrip("\n").split('\n')
	state = ''
	for line in output:
		line = line.strip()
		if line == '':
			continue
		if line[0] == 'A':
			state = 'answer'
			page(msg='')
		elif line[0] == 'Q':
			state = 'question'
			page(msg='')
		print(line)
	print('============================\nDone doing revise\n============================')


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


# Goes through notes files that changed recently
def run_notes():
	global ROOT_DIR
	global DEBUG
	page(msg='Doing notes, ret to continue')
	files = set()
	notes = []
	# Did we specify a specific number of days?
	if nday_scan_days != -1:
		cmd = '''git whatchanged --since="''' + str(nday_scan_days) + ''' days ago" --pretty=format:'' ''' + ROOT_DIR + '''/notes | grep -v '^$' | sort -u | grep -v README | grep asciidoc'''
		files = set(os.popen(cmd).read().rstrip("\n"))
	else:
		for day in days:
			cmd = '''git whatchanged --since="''' + day + ''' days ago" --until="$[''' + day + '''-1] days ago" --name-only --pretty=format:"" ''' + ROOT_DIR + '''/notes | grep asciidoc | grep -v "^$" | sort -u'''
			debug(cmd)
			new_files = set(os.popen(cmd).read().rstrip("\n").split('\n'))
			files = files.union(new_files)
	note = ''
	for f in files:
		# Redirect stderr to avoid problems when file no longer exists in git
		cmd = "git whatchanged --since=\""+day+" days ago\" --until=\"$["+day+"-1] days ago\" --patch --pretty=format:\"\" "+ROOT_DIR+"/"+f+" 2>&1 | grep '^+' | sed 's/^.//'"
		debug(cmd)
		note = os.popen(cmd).read().rstrip("\n")
		if note:
			notes += [note]
	num_items = len(notes)
	while num_items > 0:
		item_no = int(random.random() * num_items)
		item = notes[item_no]
		debug(str(num_items) + ' left')
		print(item)
		page()
		notes.remove(item)
		num_items = len(notes)
	print('============================\nDone doing notes\n============================')


def run_pop():
	global ROOT_DIR
	page(msg='Doing pop quiz, ret to continue')
	files = set()
	image_files = set()
	cmd = '''git whatchanged --name-only --pretty=format:'' ''' + ROOT_DIR + '''/learning | grep -v '^$' | sort -u | grep -v README | grep asciidoc'''
	debug(cmd)
	new_files = set(os.popen(cmd).read().rstrip("\n").split('\n'))
	files = files.union(new_files)
	debug(cmd)
	cmd = '''git whatchanged | egrep "(\.jpg$|\.png$)"'''
	new_files = set(os.popen(cmd).read().rstrip("\n").split('\n'))
	image_files = image_files.union(new_files)
	questions_from_files(files, image_files)
	print('============================\nDone doing pop quiz\n============================')


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


def debug(text):
	global DEBUG
	if DEBUG:
		print(text)


def main():
	# TODO: select subset of folders to look through
	# TODO: More descriptive picks
	global nday_scan_days
	global DEBUG
	global OS_TYPE
	print('To add a question, go to /space/git/work/learning and follow the examples, check in and push')
	options = ['qanda', 'revise', 'notes', 'popquiz', 'nday_scan', 'debug']
	res = pick.pick(options, title='Choose (space to select, return to continue)', indicator='x', multi_select=True, min_selection_count=1)
	notes        = False
	qanda        = False
	revise       = False
	pop          = False
	nday_scan    = False
	debug        = False
	for r in res:
		if r[0] == 'notes':
			notes = True
		elif r[0] == 'debug':
			DEBUG = True
		elif r[0] == 'qanda':
			qanda = True
		elif r[0] == 'revise':
			revise = True
		elif r[0] == 'popquiz':
			pop = True
		elif r[0] == 'nday_scan':
			nday_scan = True
	if nday_scan == True:
		nday_scan_days = input('Input number of days to look back at: ')
	if pop:
		run_pop()
	else:
		if revise:
			run_revise()
		if notes:
			run_notes()
		if qanda:
			run_qanda()
		if revise:
			run_revise(msg='Doing revise again. Hit return to continue')

# In debug mode?
DEBUG=False
# Number of days to scan back. Default is -1 (meaning don't)
nday_scan_days = -1

# BEGIN Set up root directory and move to it BEGIN
OS_TYPE = platform.system()
if OS_TYPE == "Darwin":
	ROOT_DIR="/Users/imiell/git/work"
elif OS_TYPE == "Linux":
	ROOT_DIR="/home/imiell/git/work"
else:
	print("OS " + OS_TYPE + " not recognised")
	sys.exit(1)
os.chdir(ROOT_DIR)
# END Set up root directory and move to it

# Prime numbers
days=['1','2','3','5','7','11','13','17','19','23','29','31','37','41','43','47','53','59','61','67','71','73','79','83','89','97','101']
# From 'How to learn'
#days=['1','2','3','5','7','14','21','28','42','56','70','84','105','126','147','168','189','219','249','279','309','339','369']
# More 'spaced out'
#days=['1','2','4','8','12','16','24','40','60','80','100','120','150','200']

main()
