import rsdb
import shared

def get_tags():
	return rsdb.get_tags()

def ask_add_tag():
	tags = get_tags()
	print_tags(tags)
	tag_to_add = ''
	while tag_to_add.strip() == '':
		tag_to_add = shared.ask('Please input tag: ')
	print('')
	notes_to_add = shared.ask('Please input notes (optional): ')
	return tag_to_add, notes_to_add

def add_tag():
	tag_to_add, notes_to_add = ask_add_tag()
	rsdb.add_tag(tag=tag_to_add, notes=notes_to_add, status='A')

def print_tags(tags):
	print('Existing tags: ')
	for tag in tags:
		print(str(tag[0]) + ': ' + tag[1])
	print('')

if __name__ == '__main__':
    add_tag()
