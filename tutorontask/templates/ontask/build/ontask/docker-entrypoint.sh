#!/bin/bash
set -e

./manage.py collectstatic --noinput

exec "$@"
