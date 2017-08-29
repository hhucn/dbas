\connect discussion;

CREATE OR REPLACE FUNCTION PUBLIC.NOTIFY() RETURNS trigger AS
$BODY$
BEGIN
PERFORM pg_notify('new_issue', row_to_json(NEW)::text);
RETURN new;
END;
$BODY$
LANGUAGE 'plpgsql' VOLATILE COST 100;

CREATE TRIGGER new_issue
AFTER INSERT or UPDATE
ON discussion.public.issues
FOR EACH ROW
EXECUTE PROCEDURE PUBLIC.NOTIFY();

