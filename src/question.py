import pick
import rsdb
import tag
import shared

def add_question():

	res = tag.choose_tags()
	# Figure out which primary key ids were picked.
	tag_ids_chosen = set()
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

	# Get question
	question = shared.ask('Please input question: ')

	# Get answer
	answer = shared.ask('Please input answer: ')

	# Insert question, and tags
	rsdb.add_question(question=question, answer=answer, tag_ids=tag_ids_chosen)


if __name__ == '__main__':
	add_question()
