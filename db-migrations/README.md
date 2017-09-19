#### Initialize database
###### `alembic stamp head`
This will set the database version to the latest revision, **without** migrating anything!


#### Create migration
###### `alembic revision --autogenerate -m "Add table X"`
Generate a new revision based on the changes in the SQLAlchemy definition.
Check the revision before using!

#### Upgrade to latest revision
###### `alembic upgrade head`
Runs all migrations until the latest revision!
Use `alembic upgrade +1` to migrate to the next revision.