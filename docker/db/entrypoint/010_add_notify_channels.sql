\connect discussion;

-- creates channels based on the table which is being watched. For example when
-- called with discussion.public.statements, the corresponding event is
-- "statements_changes"

CREATE OR REPLACE FUNCTION notify_trigger() RETURNS trigger AS $$
       DECLARE
          channel_name varchar DEFAULT (TG_TABLE_NAME || '_changes');
       BEGIN
          IF TG_OP = 'INSERT' THEN
             PERFORM pg_notify(channel_name, '{"event": "insert_' || TG_TABLE_NAME || '", "data": ' || row_to_json(NEW)::text || '}');
             RETURN NEW;
          END IF;
          IF TG_OP = 'UPDATE' THEN
             PERFORM pg_notify(channel_name, '{"event": "update_' || TG_TABLE_NAME || '", "data": ' || row_to_json(NEW)::text || '}');
             RETURN NEW;
          END IF;
       END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_statements_trigger AFTER INSERT OR UPDATE ON discussion.public.statements FOR EACH ROW EXECUTE PROCEDURE notify_trigger();
CREATE TRIGGER update_textversions_trigger AFTER INSERT OR UPDATE ON discussion.public.textversions FOR EACH ROW EXECUTE PROCEDURE notify_trigger();
CREATE TRIGGER update_arguments_trigger AFTER INSERT OR UPDATE ON discussion.public.arguments FOR EACH ROW EXECUTE PROCEDURE notify_trigger();
CREATE TRIGGER update_issues_trigger AFTER INSERT OR UPDATE ON discussion.public.issues FOR EACH ROW EXECUTE PROCEDURE notify_trigger();
CREATE TRIGGER update_users_trigger AFTER INSERT OR UPDATE ON discussion.public.users FOR EACH ROW EXECUTE PROCEDURE notify_trigger();