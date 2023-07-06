FROM docker.io/ubuntu:22.04
ENV DEBIAN_FRONTEND=noninteractive

# Project Files and Settings
ENV PROJECT=ontask
ENV PROJECT_DIR=/app/ontask
ENV PROJECT_PATH=${PROJECT_DIR}
ENV CELERY_BIN=/app/venv/bin/celery

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

###### Install python with pyenv in /opt/pyenv and create virtualenv in /ontask/venv
# https://github.com/pyenv/pyenv/wiki/Common-build-problems#prerequisites
RUN apt update && \
    apt install -y libssl-dev zlib1g-dev libbz2-dev \
    libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev \
    xz-utils tk-dev libffi-dev liblzma-dev python3-openssl git

# Install apache2
RUN apt-get update && apt-get install -y apache2 apache2-utils libapache2-mod-wsgi-py3

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
    git clone https://github.com/abelardopardo/ontask_b.git --branch Version_10_3 --depth 1 /app/ontask
WORKDIR /app/ontask

###### Copy configuration files
# Copy apache config
RUN cp /app/ontask/docker/server/000-default.conf /etc/apache2/sites-available

###### Turn on virtualenv and install requirements

# Turn on virtualenv
ENV PATH /app/venv/bin:${PATH}
ENV VIRTUAL_ENV /app/venv/

# Install Requirements
RUN pip install -r /app/ontask/requirements/base.txt
RUN pip install -r /app/ontask/requirements/essential.txt

###### Change ownership of the files
RUN chown -R www-data:www-data /app/ontask

###### Create log files
RUN mkdir -p /app/ontask/logs
RUN echo "Touching log files" \
touch /app/ontask/logs/django.log \
touch /app/ontask/logs/project.log \
touch /app/ontask/logs/scheduler.log \
touch /app/ontask/logs/script.log \
touch /app/ontask/logs/celery.log

EXPOSE 8080

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]
