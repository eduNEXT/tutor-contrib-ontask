FROM ubuntu:20.04

LABEL Abelardo Pardo

# Project Files and Settings
ENV PROJECT=ontask
ARG PROJECT=ontask
ARG PROJECT_DIR=/data/web
ENV PROJECT_DIR=${PROJECT_DIR}
ENV PROJECT_PATH=${PROJECT_DIR}
ENV CELERY_BIN=/usr/local/bin/celery
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND=noninteractive

# Set up packages
RUN apt-get -yqq update && \
    apt-get install -y software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt-get -yqq update && \
    apt-get install -yqq \
      apache2 \
      apache2-utils \
      apt-utils \
      curl \
      dialog \
      libapache2-mod-wsgi-py3 \
      python3 \
      python3.9-dev \
      python3.9-distutils \
      python3-pip \
      postgresql-client \
      libpq-dev \
      rsync \
      vim \
&& rm -rf /var/lib/apt/lists/*

# Copy apache config
COPY docker/server/000-default.conf /etc/apache2/sites-available

# Get pip
RUN python3.9 -m pip install --no-cache-dir --upgrade pip

# Create directory and copy django project
RUN mkdir -p $PROJECT_DIR
WORKDIR $PROJECT_DIR
COPY --chown=www-data:www-data . $PROJECT_DIR

# Install Requirements
RUN python3.9 -m pip install --no-cache-dir --upgrade -r requirements/development.txt

# Generate the documentation (so that this step is not repeated if restarting)
WORKDIR $PROJECT_DIR/docs_src
# RUN make copy_to_docs

ENTRYPOINT ["/data/web/docker/server/docker-entrypoint.sh"]

CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]

EXPOSE 80
