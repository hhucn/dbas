\connect discussion

BEGIN;

-- Running upgrade ed3484af5b24 -> 45be64188139

ALTER TABLE statements RENAME COLUMN is_startpoint TO is_position;

UPDATE alembic_version SET version_num='45be64188139' WHERE alembic_version.version_num = 'ed3484af5b24';

COMMIT;
