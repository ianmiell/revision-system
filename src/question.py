import rsdb
import tag
import shared


def add_question():
	shared.clear_screen()
	result, tag_ids_chosen = choose_tags()
	if not result:
		return
	while True:
		# Get question
		question = shared.ask('Please input question to add: ')
		# Get answer
		answer = shared.ask('Please input answer: ')
		# Insert question, and tags
		rsdb.add_question(question=question, answer=answer, tag_ids=list(tag_ids_chosen))
		do_continue = shared.ask_continue('Add another question with these tags (y/n)?')
		if not do_continue:
			break


def choose_tags():
	tags = tag.get_tags()
	result, res  = tag.choose_tags()
	if not result:
		return False, None
	# Figure out which primary key ids were picked.
	tag_ids_chosen     = set()
	tag_indexes_chosen = set()
	# Get the choices made from the index of choices
	for tag_chosen in res:
		tag_indexes_chosen.add(tag_chosen[1])
	# Get the actual primary key ids from the choices made
	for tag_indexes_choice in tag_indexes_chosen:
		tag_ids_chosen.add(tags[tag_indexes_choice][0])
	tag_chosen         = None
	tag_indexes_chosen = None
	tag_indexes_choice = None
	return True, tag_ids_chosen


# This option exists for deprecated question files in old version of this application.
def bulk_insert():
	result, tag_ids_chosen = choose_tags()
	if not result:
		return False
	filename = shared.ask('\n\nPlease input filename: ')
	for line in open(filename, 'r').readlines():
		print(line)
		if line[:2] == 'Q:' or line[:2] == 'q:':
			question = line[3:]
		if line[:2] == 'A:' or line[:2] == 'a':
			answer = line[3:]
			rsdb.add_question(question=question, answer=answer, tag_ids=tag_ids_chosen)
			print('Added: ' + question + ' with answer: ' + answer)
	return True


if __name__ == '__main__':
	add_question()
