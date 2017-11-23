\connect discussion

BEGIN;

-- Running upgrade 2a4bc7c8ff38 -> 42d481d084b2

ALTER TABLE users ADD COLUMN oauth_provider TEXT;

ALTER TABLE users ADD COLUMN oauth_provider_id TEXT;

UPDATE alembic_version SET version_num='42d481d084b2' WHERE alembic_version.version_num = '2a4bc7c8ff38';

COMMIT;
