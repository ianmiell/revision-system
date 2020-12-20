import sqlite3
#import datetime

def get_conn():
	conn = sqlite3.connect('db/revision-system.db')
	c = conn.cursor()
	return conn, c

def commit_and_close_conn(conn):
	conn.commit()
	conn.close()

def run_qry(qry_str, args=None):
	conn, c = get_conn()
	if args is None:
		ret = c.execute(qry_str)
	else:
		ret = c.execute(qry_str, args)
	commit_and_close_conn(conn)
	return ret

def fetchone(qry_str, args):
	conn, c = get_conn()
	result = c.execute(qry_str, args).fetchone()
	commit_and_close_conn(conn)
	return result

def get_tags():
	conn, c = get_conn()
	c.execute('select tag_id, tag, notes, status from tag')
	tags = []
	for tags in c:
		tags.append(tags)
	commit_and_close_conn(conn)
	return tags

# TODO: handle dupe
def add_tag(tag_text, notes, status='A'):
	conn, c = get_conn()
	c.execute('insert into tag (tag, notes, status) values(?, ?, ?)', (tag, notes, status))
	# Get the id
	tag_id = c.lastrowid
	commit_and_close_conn(conn)
	return True, tag_id

# TODO: handle dupe
def add_question(question, answer, category, tag_id):
	conn, c = get_conn()
	# Insert the question, then get the id
	c.execute('insert into question (question, answer) values(?, ?)', (question, answer))
	# Get the id
	question_id = c.lastrowid
	# Insert question_tag
	c.execute('insert into question_tag (question_id, tag_id) values(?, ?)', (question_id, tag_id))
	commit_and_close_conn(conn)
	return True, question_id

# Examples:
#def get_following_me(user_id):
#	result = fetchone('select following_me from twitter_user where user_id = ?', (user_id,))
#	following_me = result[0]
#	return following_me

#def update_following_me(user_id, to):
#	run_qry('update twitter_user set following_me = ? where user_id = ?', (to, user_id))

#def get_top_followers():
#	conn, c = get_conn()
#	c.execute('select handle, num_followers, following_me from twitter_user where ignored = "N" and following_me = "Y" order by {0} desc'.format('num_followers'))
#	users = []
#	for user in c:
#		users.append(user)
#	commit_and_close_conn(conn)
#	return users

#def is_user_in_system(user_id):
#	conn, c = get_conn()
#	numrows = -1
#	qry = "select count(1) from twitter_user where user_id = ?"
#	twitter_shared.myprint('qry: ' + qry + ' user: ' + str(user_id), loglevel=10)
#	c.execute(qry, (user_id,))
#	result = c.fetchone()
#	numrows = result[0]
#	commit_and_close_conn(conn)
#	return numrows > 0

#def insert_or_update_user(user_id, screen_name=None, followers_count=None, following_me='N', last_active=-1, following=None):
#	conn, c = get_conn()
#	numrows = -1
#	c.execute('select count(1) from twitter_user where user_id = ?', (user_id,))
#	result = c.fetchone()
#	# Passing these in as 'None' means 'update if a row is found, as we want to ignore this for a while', eg if it's blocked us.
#	if screen_name is None and followers_count is None:
#		if len(result) != 0:
#			conn, c = get_conn()
#			if following is None:
#				c.execute('update twitter_user set last_updated = ? where user_id = ?', (datetime.datetime.now(), user_id))
#			else:
#				c.execute('update twitter_user set last_updated = ?, following = ? where user_id = ?', (datetime.datetime.now(), following, user_id))
#			commit_and_close_conn(conn)
#		return
#	numrows = result[0]
#	commit_and_close_conn(conn)
#	if numrows == 0:
#		conn, c = get_conn()
#		if following is None:
#			c.execute('insert into twitter_user (user_id, handle, num_followers, following_me, last_active) values(?, ?, ?, ?, ?)', (user_id, screen_name, followers_count, following_me, last_active))
#		else:
#			c.execute('insert into twitter_user (user_id, handle, num_followers, following_me, last_active, following) values(?, ?, ?, ?, ?, ?)', (user_id, screen_name, followers_count, following_me, last_active, following))
#		commit_and_close_conn(conn)
#	elif numrows == 1:
#		conn, c = get_conn()
#		if following is None:
#			c.execute('update twitter_user set handle = ?, num_followers = ?, last_updated = ?, last_active = ? where user_id = ?', (screen_name, followers_count, datetime.datetime.now(), last_active, user_id))
#		else:
#			c.execute('update twitter_user set handle = ?, num_followers = ?, last_updated = ?, last_active = ?, following = ? where user_id = ?', (screen_name, followers_count, datetime.datetime.now(), last_active, following, user_id))
#		commit_and_close_conn(conn)
