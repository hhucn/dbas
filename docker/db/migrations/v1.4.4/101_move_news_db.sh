#!/usr/bin/env bash

pg_dump -U postgres -t news news | psql -U postgres discussion
dropdb news