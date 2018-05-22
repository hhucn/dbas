#!/bin/bash

bash build_assets.sh
alembic upgrade head
pserve development.ini --reload