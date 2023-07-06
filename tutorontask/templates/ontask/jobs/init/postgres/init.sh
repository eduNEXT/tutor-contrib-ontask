#!/bin/sh

# Check if the user already exists
EXISTING_USER=$(PGPASSWORD={{ ONTASK_POSTGRES_ROOT_PASSWORD }} psql -h {{ ONTASK_POSTGRES_HOST }} -p 5432 -U {{ ONTASK_POSTGRES_ROOT_USERNAME }} -tAc "SELECT 1 FROM pg_roles WHERE rolname='{{ ONTASK_DB_USER }}'")

if [ "$EXISTING_USER" -gt 0 ]; then
  echo "User '$USERNAME' already exists. Skipping user creation."
else
    PGPASSWORD={{ ONTASK_POSTGRES_ROOT_PASSWORD }} psql -h {{ ONTASK_POSTGRES_HOST }} -p 5432 -U {{ ONTASK_POSTGRES_ROOT_USERNAME }} -c "CREATE USER {{ ONTASK_DB_USER }}"
    PGPASSWORD={{ ONTASK_POSTGRES_ROOT_PASSWORD }} psql -h {{ ONTASK_POSTGRES_HOST }} -p 5432 -U {{ ONTASK_POSTGRES_ROOT_USERNAME }} -c "ALTER USER {{ ONTASK_DB_USER }} WITH PASSWORD '{{ ONTASK_POSTGRES_PASSWORD }}'"
fi

EXISTING_DB=$(PGPASSWORD={{ ONTASK_POSTGRES_ROOT_PASSWORD }} psql -h {{ ONTASK_POSTGRES_HOST }} -p 5432 -U {{ ONTASK_POSTGRES_ROOT_USERNAME }} -lqt | cut -d \| -f 1 | grep -wq "{{ ONTASK_DB_NAME }}" && echo "1" || echo "0")

if [ "$EXISTING_DB" -gt 0 ]; then
  echo "Database '{{ ONTASK_DB_NAME }}' already exists. Skipping database creation."
else
  # Create the database
  PGPASSWORD={{ ONTASK_POSTGRES_ROOT_PASSWORD }} psql -h {{ ONTASK_POSTGRES_HOST }} -p 5432 -U {{ ONTASK_POSTGRES_ROOT_USERNAME }} -c "CREATE DATABASE {{ ONTASK_DB_NAME }} OWNER {{ ONTASK_DB_USER }}"
  echo "Database '{{ ONTASK_DB_NAME }}' created successfully."
fi
