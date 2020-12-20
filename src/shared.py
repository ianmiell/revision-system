#!/usr/bin/env python3

def page(msg='[Hit enter to continue]'):
	return ask(msg)

def debug(text):
	global DEBUG
	if DEBUG:
		print(text)

def ask(msg=''):
	if msg != '':
		print(msg)
	return input()


DEBUG = False
