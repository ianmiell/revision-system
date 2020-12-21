.PHONY: run clean init_db start save_state safe_clean

run: check_run safe_clean init_db start save_state safe_clean

clean: init_db

init_db: safe_clean
	cat db/db_export.sql | sqlite3 db/revision-system.db

start:
	python3 src/main.py || python src/main.py

save_state:
	echo ".dump" | sqlite3 db/revision-system.db > db/db_export.sql
	git commit -am "saving state" || true
	git pull --rebase -s recursive -X ours
	git push

check_run:
	type git > /dev/null || echo Need git installed
	type python3 > /dev/null || type python > /dev/null || echo Need python version installed
	type sqlite3 > /dev/null || echo Need sqlite3 installed

# Removes everything (tho we still have git history).
# Removes data that is recreated with a make
safe_clean:
	rm -f db/revision-system.db
