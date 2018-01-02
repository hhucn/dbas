#!/bin/bash

sleep 8
alembic upgrade head
pserve development.ini --reload
