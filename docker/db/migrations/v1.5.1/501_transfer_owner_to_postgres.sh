# ALTER public schema
for tbl in `psql -qAt -U postgres -c "select tablename from pg_tables where schemaname = 'public';" discussion` ; do  psql -U postgres -c "alter table \"$tbl\" owner to postgres" discussion ; done

# ALTER news schema
for tbl in `psql -qAt -U postgres -c "select tablename from pg_tables where schemaname = 'news';" discussion` ; do  psql -U postgres -c "alter table news.\"$tbl\" owner to postgres" discussion ; done

dropuser -U postgres --if-exists dbas
dropuser -U postgres --if-exists writer
dropuser -U postgres --if-exists read_only_discussion