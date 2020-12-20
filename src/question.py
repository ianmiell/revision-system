import pick
import rsdb
import tag
import shared

def add_question():
	# Get tags
	tags = tag.get_tags()
	tag.print_tags(tags)

	# Pick tags
	options = []
	[ options.append(x[1]) for x in tags ]
	res = pick.pick(options, title='Choose (space to select, return to continue)', indicator='x', multi_select=True, min_selection_count=1)

	# Figure out which primary key ids were picked.
	tag_ids_chosen = set()
	tag_indexes_chosen = set()
	# Get the choices made from the index of choices
	for tag_chosen in res:
		tag_indexes_chosen.add(tag_chosen[1])
	# Get the actual primary key ids from the choices made
	for tag_indexes_choice in tag_indexes_chosen:
		tag_ids_chosen.add(tags[tag_indexes_choice][0])
	print(tag_indexes_choice)
	tag_chosen         = None
	tag_indexes_chosen = None
	tag_indexes_choice = None

	# Get question
	question = shared.ask('Please input question: ')

	# Get answer
	answer = shared.ask('Please input answer: ')

	# Insert question, and tags
	rsdb.add_question(question=question, answer=answer, tag_ids=tag_ids_chosen)


if __name__ == '__main__':
	add_question()
