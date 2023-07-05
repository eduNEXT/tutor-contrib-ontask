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
RUN apt-get update && apt upgrade -y \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y postgresql-client libpq-dev \
  # mysql dependencies
  # && apt-get install -y default-mysql-client default-libmysqlclient-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Install Requirements + supervisor
COPY ./requirements/ /requirements/
RUN python -m pip install --no-cache-dir --upgrade -r requirements/development.txt \
  && python -m pip install --no-cache-dir --upgrade supervisor

# Copy Django project
WORKDIR $PROJECT_DIR
COPY . $PROJECT_DIR

CMD ["/usr/local/bin/supervisord", "-n" ,"-c", "/app/supervisor/supervisor.conf"]