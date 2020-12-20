import subprocess
import platform

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


def clear_screen():
	if platform.system()=="Windows":
		subprocess.Popen("cls", shell=True).communicate() #I like to use this instead of subprocess.call since for multi-word commands you can just type it out, granted this is just cls and subprocess.call should work fine
	else: #Linux and Mac
		print("\033c", end="")


DEBUG = False
