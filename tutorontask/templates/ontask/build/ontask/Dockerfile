FROM python:3.9-slim-buster

# Python Envs
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Project Files and Settings
ENV PROJECT=ontask
ENV PROJECT_DIR=/app
ENV PROJECT_PATH=${PROJECT_DIR}
ENV CELERY_BIN=/usr/local/bin/celery

# Set up packages
RUN apt-get update && apt-get upgrade -y \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y postgresql-client libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Install Requirements
COPY ./requirements/ /requirements/
RUN pip install -r /requirements/development.txt

COPY ./docker/server/docker-entrypoint.sh /docker-entrypoint.sh
RUN sed -i 's/\r$//g' /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

COPY ./docker/server/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# Copy Django project
WORKDIR $PROJECT_DIR
COPY . $PROJECT_DIR

ENTRYPOINT ["/docker-entrypoint.sh"]