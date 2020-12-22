import subprocess
import platform
import colorit
import hashlib
import readline

def page(msg='[Hit enter to continue]'):
	return ask(msg)


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


def strikethrough(msg):
	return colorit.strike(msg)


def hash_color_string(msg, bold=True, strikethrough=False, underline=False):
	hash_val = int(hashlib.sha256(msg.encode('utf-8')).hexdigest(), 16) % 10**1
	green  = [0,   128, 0]
	blue   = [0,   0,   255]
	red    = [255, 0,   0]
	yellow = [255, 255, 0]
	white  = [255, 255, 255]
	if hash_val == 0:
		back  = yellow
		front = red
	elif hash_val == 1:
		back  = red
		front = yellow
	elif hash_val == 2:
		back  = green
		front = white
	elif hash_val == 3:
		back  = white
		front = blue
	elif hash_val == 4:
		back  = white
		front = red
	elif hash_val == 5:
		back  = red
		front = white
	elif hash_val == 6:
		back  = yellow
		front = blue
	elif hash_val == 7:
		back  = blue
		front = yellow
	elif hash_val == 8:
		back  = blue
		front = white
	elif hash_val == 9:
		back  = yellow
		front = green
	to_print = colorit.color_front(colorit.color_back(msg, back[0], back[1], back[2]), front[0], front[1], front[2])
	if bold:
		to_print = colorit.bold(to_print)
	if strikethrough:
		to_print = colorit.strike(to_print)
	if underline:
		to_print = colorit.under(to_print)
	return to_print
