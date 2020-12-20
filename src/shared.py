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


def get_option_description(option):
    return option.get('description')


def ask_continue(msg):
	response = ask(msg)
	if response in ('y', 'Y', 'yes', 'YES'):
		return True
	else:
		return False


DEBUG = False
