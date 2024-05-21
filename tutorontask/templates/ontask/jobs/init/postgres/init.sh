#!/bin/sh

# Function to check if PostgreSQL is available
check_postgres() {
  PGPASSWORD={{ ONTASK_POSTGRES_ROOT_PASSWORD }} pg_isready -h {{ ONTASK_POSTGRES_HOST }} -p 5432 -U {{ ONTASK_POSTGRES_ROOT_USERNAME }}
}

# Wait for PostgreSQL to become available with a timeout of 60 seconds
timeout=60
while ! check_postgres; do
  sleep 1
  timeout=$((timeout - 1))
  if [ $timeout -eq 0 ]; then
    echo "Timeout: PostgreSQL is not available."
    exit 1
  fi
done

# Check if the user already exists
EXISTING_USER=$(PGPASSWORD={{ ONTASK_POSTGRES_ROOT_PASSWORD }} psql -h {{ ONTASK_POSTGRES_HOST }} -p 5432 -U {{ ONTASK_POSTGRES_ROOT_USERNAME }} -tAc "SELECT 1 FROM pg_roles WHERE rolname='{{ ONTASK_DB_USER }}'")

if [ "$EXISTING_USER" -gt 0 ]; then
  echo "User '{{ ONTASK_DB_USER }}' already exists. Skipping user creation."
else
  PGPASSWORD={{ ONTASK_POSTGRES_ROOT_PASSWORD }} psql -h {{ ONTASK_POSTGRES_HOST }} -p 5432 -U {{ ONTASK_POSTGRES_ROOT_USERNAME }} -c "CREATE USER {{ ONTASK_DB_USER }}"
  PGPASSWORD={{ ONTASK_POSTGRES_ROOT_PASSWORD }} psql -h {{ ONTASK_POSTGRES_HOST }} -p 5432 -U {{ ONTASK_POSTGRES_ROOT_USERNAME }} -c "ALTER USER {{ ONTASK_DB_USER }} WITH PASSWORD '{{ ONTASK_DB_PASSWORD }}'"
fi

EXISTING_DB=$(PGPASSWORD={{ ONTASK_POSTGRES_ROOT_PASSWORD }} psql -h {{ ONTASK_POSTGRES_HOST }} -p 5432 -U {{ ONTASK_POSTGRES_ROOT_USERNAME }} -lqt | cut -d \| -f 1 | grep -wq "{{ ONTASK_DB_NAME }}" && echo "1" || echo "0")

if [ "$EXISTING_DB" -gt 0 ]; then
  echo "Database '{{ ONTASK_DB_NAME }}' already exists. Skipping database creation."
else
  # Create the database
  PGPASSWORD={{ ONTASK_POSTGRES_ROOT_PASSWORD }} psql -h {{ ONTASK_POSTGRES_HOST }} -p 5432 -U {{ ONTASK_POSTGRES_ROOT_USERNAME }} -c "CREATE DATABASE {{ ONTASK_DB_NAME }} OWNER {{ ONTASK_DB_USER }}"
  echo "Database '{{ ONTASK_DB_NAME }}' created successfully."
fi
