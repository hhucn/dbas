BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL,
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running stamp_revision  -> 2a4bc7c8ff38

INSERT INTO alembic_version (version_num) VALUES ('2a4bc7c8ff38');

COMMIT;