import pick
import rsdb
import shared


def get_tags():
	return rsdb.get_tags()


def ask_add_tag():
	shared.clear_screen()
	tags = get_tags()
	print_tags(tags)
	tag_to_add = ''
	while tag_to_add.strip() == '':
		tag_to_add = shared.ask('Please input tag: ')
	print('')
	notes_to_add = shared.ask('Please input notes (optional): ')
	return tag_to_add, notes_to_add


def add_tag():
	while True:
		tag_to_add, notes_to_add = ask_add_tag()
		rsdb.add_tag(tag=tag_to_add, notes=notes_to_add, status='A')
		if not shared.ask_continue('Add another tag? (y/n)'):
			break


def print_tags(tags):
	print('Existing tags: ')
	for tag in tags:
		print(str(tag[0]) + ': ' + tag[1])
	print('')


def choose_tags():
	shared.clear_screen()
	# Get tags
	tags = get_tags()
	# Pick tags
	options = []
	[ options.append(x[1]) for x in tags ]
	res = pick.pick(options, title='Choose tags (space to select, return to continue)', indicator='x', multi_select=True, min_selection_count=1)
	assert isinstance(res, list)
	for item in res:
		assert isinstance(item, tuple)
	return res


if __name__ == '__main__':
    add_tag()
