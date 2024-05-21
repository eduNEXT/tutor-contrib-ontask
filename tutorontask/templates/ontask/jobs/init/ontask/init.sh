# Wait for the database to be up and running
until psql {{ ONTASK_DATABASE_URL }} -c '\l'; do
 >&2 echo "Postgres is not available in {{ ONTASK_DATABASE_URL }} - sleeping"
 sleep 3
done

>&2 echo "Postgres is up in {{ ONTASK_DATABASE_URL }} - continuing"

>&2 echo "Migrating"
./manage.py migrate --noinput

>&2 echo "Creating initial data (instructors)"
./manage.py initialize_db -i /app/ontask/scripts/initial_instructors.csv

>&2 echo "Creating initial data (learners)"
./manage.py initialize_db /app/ontask/scripts/initial_learners.csv

>&2 echo "Creating superuser "
./manage.py create_superuser -u {{ ONTASK_SUPERUSER_NAME }} -e {{ ONTASK_SUPERUSER_EMAIL }} -p {{ ONTASK_SUPERUSER_PASSWORD }}
