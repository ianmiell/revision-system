#!/usr/bin/env python3
import pick
import qanda

def main():
	# TODO: select subset of folders to look through
	# TODO: More descriptive picks
	global nday_scan_days
	global DEBUG
	print('To add a question, go to /space/git/work/learning and follow the examples, check in and push')
	options = ['qanda', 'revise', 'notes', 'popquiz', 'nday_scan', 'debug']
	res = pick.pick(options, title='Choose (space to select, return to continue)', indicator='x', multi_select=True, min_selection_count=1)
	notes        = False
	qanda        = False
	revise       = False
	pop          = False
	nday_scan    = False
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
	if nday_scan:
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

# Prime numbers
days=['1','2','3','5','7','11','13','17','19','23','29','31','37','41','43','47','53','59','61','67','71','73','79','83','89','97','101']
# From 'How to learn'
#days=['1','2','3','5','7','14','21','28','42','56','70','84','105','126','147','168','189','219','249','279','309','339','369']
# More 'spaced out'
#days=['1','2','4','8','12','16','24','40','60','80','100','120','150','200']

main()
