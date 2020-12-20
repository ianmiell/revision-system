clean: safe_clean init_db

run: safe_clean init_db start save_state safe_clean

init_db:
	cat db/db_export.sql | sqlite3 db/rs.db

start:
	echo 'start'

save_state:
	echo ".dump" | sqlite3 db/rs.db > db/db_export.sql
	git commit -am "saving state" || true
	git pull --rebase -s recursive -X ours
	git push

# Removes everything (tho we still have git history).
# Removes data that is recreated with a make
safe_clean:
	rm -f db/rs.db
