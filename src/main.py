#!/usr/bin/env python3
import pick
import sys
import qanda
import tag
import question
import shared

def main():
	# TODO: select subset of folders to look through
	# TODO: More descriptive picks
	options = ['qanda', 'revise', 'debug', 'add_question', 'add_tag']
	res = pick.pick(options, title='Choose (space to select, return to continue)', indicator='x', multi_select=True, min_selection_count=1)
	#notes        = False
	do_qanda        = False
	revise       = False
	add_question = False
	add_tag = False
	for r in res:
		#if r[0] == 'notes':
		#	notes = True
		if r[0] == 'debug':
			shared.DEBUG = True
		elif r[0] == 'qanda':
			do_qanda = True
		elif r[0] == 'revise':
			revise = True
		elif r[0] == 'add_question':
			add_question = True
		elif r[0] == 'add_tag':
			add_tag = True
	if revise:
		run_revise()
	if do_qanda:
		qanda.run_qanda()
	if revise:
		run_revise(msg='Doing revise again. Hit return to continue')
	if add_question:
		question.add_question()
	if add_tag:
		tag.add_tag()

if __name__ == '__main__':
	if sys.version_info.major == 2:
		print('Must be python3')
		sys.exit(1)
	main()
