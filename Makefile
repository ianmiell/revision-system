run: safe_clean init_db start save_state safe_clean

clean: safe_clean init_db

init_db:
	cat db/db_export.sql | sqlite3 db/revision-system.db

start:
	python3 src/main.py

save_state:
	echo ".dump" | sqlite3 db/revision-system.db > db/db_export.sql
	# Not ready yet!
	git commit -am "saving state" || true
	git pull --rebase -s recursive -X ours
	git push

# Removes everything (tho we still have git history).
# Removes data that is recreated with a make
safe_clean:
	rm -f db/revision-system.db
