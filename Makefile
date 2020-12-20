run: init_db start save safe_clean

init_db:
	rm -f db/rs.db
	cat db/db_export.sql | sqlite3 db/rs.db

start:
	echo 'start'

save:
	echo ".dump" | sqlite3 db/rs.db > db/db_export.sql
	git commit -am re-run || true
	git pull --rebase -s recursive -X ours
	git push

# Removes everything (tho we still have git history).
# Removes data that is recreated with a make
safe_clean:
	rm -f db/rs.db
	cp /dev/null db/db_export.db
