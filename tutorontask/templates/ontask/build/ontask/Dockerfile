FROM docker.io/ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# Project Files and Settings
ENV PROJECT=ontask
ENV PROJECT_DIR=/app/ontask
ENV PROJECT_PATH=${PROJECT_DIR}
ENV CELERY_BIN=/app/venv/bin/celery
ENV ENV_FILENAME=/app/ontask/docker.env

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

###### Install required packages

# Install python with pyenv in /opt/pyenv and create virtualenv in /ontask/venv
# https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites
RUN apt update && \
    apt install -y libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git pkg-config libmysqlclient-dev

# Install pyenv
# https://www.python.org/downloads/
# https://github.com/pyenv/pyenv/releases
ARG PYTHON_VERSION=3.9.17
ENV PYENV_ROOT /opt/pyenv
RUN git clone https://github.com/pyenv/pyenv $PYENV_ROOT --branch v2.3.21 --depth 1

# Install Python
RUN $PYENV_ROOT/bin/pyenv install $PYTHON_VERSION

# Create virtualenv
RUN $PYENV_ROOT/versions/$PYTHON_VERSION/bin/python -m venv /app/venv

###### Checkout OnTask code

RUN mkdir -p /app/ontask && \
    git clone https://github.com/abelardopardo/ontask_b.git --branch {{ ONTASK_APP_VERSION }} --depth 1 /app/ontask
WORKDIR /app/ontask

###### Turn on virtualenv and install requirements

# Turn on virtualenv
ENV PATH /app/venv/bin:${PATH}
ENV VIRTUAL_ENV /app/venv/

# Install Requirements
RUN pip install -r /app/ontask/requirements/base.txt
RUN pip install -r /app/ontask/requirements/essential.txt
RUN pip install uwsgi==2.0.21
RUN pip install PyMySQL==1.1.1

# Copy the default uWSGI configuration
COPY settings/uwsgi.ini .

###### Set entrypoint

# Copy the entrypoint file
COPY docker-entrypoint.sh /usr/local/bin/

# Set the executable permission for the entrypoint file
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["docker-entrypoint.sh"]

###### Set CMD
CMD uwsgi uwsgi.ini

EXPOSE 8080
