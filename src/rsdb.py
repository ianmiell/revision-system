import sqlite3


def get_conn():
	conn = sqlite3.connect('db/revision-system.db')
	c = conn.cursor()
	return conn, c


def commit_and_close_conn(conn):
	conn.commit()
	conn.close()


def run_qry(qry_str, args=None):
	assert isinstance(qry_str, str)
	conn, c = get_conn()
	if args is None:
		ret = c.execute(qry_str)
	else:
		ret = c.execute(qry_str, args)
	commit_and_close_conn(conn)
	return ret


def fetchone(qry_str, args):
	assert isinstance(qry_str, str)
	conn, c = get_conn()
	result = c.execute(qry_str, args).fetchone()
	commit_and_close_conn(conn)
	return result


def get_tags():
	conn, c = get_conn()
	c.execute('select tag_id, tag, notes, status from tag')
	tags = []
	for row in c:
		tags.append(row)
	commit_and_close_conn(conn)
	return tags


# TODO: handle dupe
def add_tag(tag, notes, status='A'):
	assert isinstance(tag, str)
	assert isinstance(notes, str)
	assert isinstance(status, str)
	conn, c = get_conn()
	c.execute('insert into tag (tag, notes, status) values(?, ?, ?)', (tag, notes, status))
	# Get the id
	tag_id = c.lastrowid
	commit_and_close_conn(conn)
	return True, tag_id


# TODO: handle dupe
def add_question(question, answer, tag_ids):
	assert isinstance(question, str)
	assert isinstance(answer, str)
	assert isinstance(tag_ids, list)
	conn, c = get_conn()
	# Insert the question, then get the id
	c.execute('insert into question (question, answer) values(?, ?)', (question, answer))
	# Get the id
	question_id = c.lastrowid
	for tag_id in tag_ids:
		# Insert question_tag
		c.execute('insert into question_tag (question_id, tag_id) values(?, ?)', (question_id, tag_id))
	commit_and_close_conn(conn)
	return True, question_id


def add_question_tags(question_id, tag_ids):
	assert isinstance(question_id, int)
	assert isinstance(tag_ids, list)
	conn, c = get_conn()
	for tag_id in tag_ids:
		c.execute('insert or replace into question_tag (question_id, tag_id) values(?, ?)', (question_id, tag_id))
	commit_and_close_conn(conn)


def get_related_questions(tag_ids, status=None):
	assert isinstance(tag_ids, list)
	assert isinstance(status, str) or status is None
	# By default, active questions only.
	conn, c = get_conn()
	if status is None:
		status = 'A'
	questions = set()
	for tag_id in tag_ids:
		for row in c.execute('select question_id from question_tag where tag_id = ?', (tag_id,)):
			questions.add(row[0])
	commit_and_close_conn(conn)
	return list(questions)


def get_question_age(question_id):
	assert isinstance(question_id, int)
	conn, c = get_conn()
	c.execute(r'''select (strftime('%s','now') - strftime('%s',date_added)) / 60 / 60 / 24 from question where question_id = ?''', (question_id,))
	age = c.fetchone()[0]
	commit_and_close_conn(conn)
	return age


def get_times_asked(question_id):
	assert isinstance(question_id, int)
	conn, c = get_conn()
	c.execute(r'''select count(*) from answer where question_id = ?''', (question_id,))
	times_asked = c.fetchone()[0]
	commit_and_close_conn(conn)
	return times_asked


def get_question_status(question_id):
	assert isinstance(question_id, int)
	conn, c = get_conn()
	c.execute(r'''select status from question where question_id = ?''', (question_id,))
	question_status = c.fetchone()[0]
	commit_and_close_conn(conn)
	return question_status


def get_ask_after(question_id):
	assert isinstance(question_id, int)
	conn, c = get_conn()
	c.execute(r'''select ask_after from question where question_id = ?''', (question_id,))
	ask_after = c.fetchone()[0]
	commit_and_close_conn(conn)
	return ask_after


def get_question(question_id):
	assert isinstance(question_id, int)
	conn, c = get_conn()
	c.execute('select question_id, question, answer, status from question where question_id = ?',(question_id,))
	question = c.fetchone()
	commit_and_close_conn(conn)
	return question


def get_question_history(question_id):
	assert isinstance(question_id, int)
	conn, c = get_conn()
	c.execute('select date_added, question, answer from question where question_id = ?',(question_id,))
	res = c.fetchone()
	date_added = res[0]
	question   = res[1]
	answer     = res[2]
	answers = list()
	for row in c.execute('select date_answered, result from answer where question_id = ?',(question_id,)):
		answers.append(row)
	commit_and_close_conn(conn)
	return date_added, question, answer, answers


def insert_answer(question_id, result):
	assert isinstance(question_id, int)
	assert result in ('R', 'W')
	run_qry('''insert into answer (question_id, result) values (?, ?)''',(question_id, result))


def update_question_status(question_id, status):
	assert isinstance(question_id, int)
	assert status in ('A', 'I', 'R')
	run_qry('''update question set status = ? where question_id = ?''',(status, question_id))


def update_question(question_id, question):
	assert isinstance(question_id, int)
	assert isinstance(question, str)
	run_qry('''update question set question = ? where question_id = ?''', (question, question_id))


def update_answer(question_id, answer):
	assert isinstance(question_id, int)
	assert isinstance(answer, str)
	run_qry('''update question set answer = ? where question_id = ?''', (answer, question_id))


def delete_question(question_id):
	assert isinstance(question_id, int)
	conn, c = get_conn()
	run_qry('''delete from question_tag where question_id = ?''', (question_id,))
	run_qry('''delete from answer where question_id = ?''', (question_id,))
	run_qry('''delete from question where question_id = ?''', (question_id,))
	commit_and_close_conn(conn)


def update_question_ask_after(question_id, days):
	assert isinstance(question_id, int)
	assert isinstance(days, int)
	run_qry('''update question set ask_after = DATE('now', '+{0} day') where question_id = ?'''.format(str(days)), (question_id,))



if __name__ == '__main__':
	#
	print(get_question_age(1))
	print(get_question_status(1))
	print(get_times_asked(1))

