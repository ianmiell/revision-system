#!/usr/bin/env python3
import sys

def page(msg='[Hit enter to continue]'):
	if msg != '':
		print(msg)
	if sys.version_info.major == 2:
		raw_input()
	else:
		input()

def debug(text):
	global DEBUG
	if DEBUG:
		print(text)

DEBUG = False
