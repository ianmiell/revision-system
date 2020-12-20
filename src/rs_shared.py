import datetime
import sys
import os.path
import rsdb

def handle_error(inst):
	myprint(str(sys.exc_info()))
	if type(inst).__name__ in ('ConnectionError','requests.exceptions.ConnectionError'):
		return 'CONNECTION_ERROR', None, ''
	myprint('error not recognised')
	myprint(inst)
	sys.exit(1)
	#import pdb
	#pdb.set_trace()

def myprint(msg, filename='logfile', loglevel=5):
	global global_loglevel
	if loglevel <= global_loglevel:
		if sys.version_info >= (3, 0):
			t=str(datetime.datetime.now())
		else:
			t=unicode(str(datetime.datetime.now()))
			try:
				msg=unicode(msg)
			except UnicodeDecodeError:
				print(msg)
				raise
		print(t + u': ' + msg)
		if filename:
			if not os.path.isfile(filename):
				f=open(filename,"w+")
				f.close()
			with open(filename, "a+") as myfile:
				myfile.write(msg.encode('utf-8') + '\n')

def set_global_loglevel(level):
	global global_loglevel
	global_loglevel = level

global_loglevel=5
