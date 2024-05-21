OnTask plugin for `Tutor <https://docs.tutor.overhang.io>`__
============================================================

`OnTask <https://www.ontasklearning.org/>`__  is a platform offering instructors and educational designers the capacity to use data to personalize the learner experience. This Tutor plugin allows you to install OnTask in your Tutor ecosystem.

**NOTE**: The OnTask service can then be integrated into the Open edX platform with the  `OnTask Plugin <https://github.com/eduNEXT/platform-plugin-ontask>`_.

This plugin is an open-source contribution to the Open edX platform ecosystem, funded by the Unidigital project from the Spanish Government - 2023.


Installation
------------

::

    pip install git+https://github.com/eduNEXT/tutor-contrib-ontask

Usage
-----

Enable the plugin::

    tutor plugins enable ontask

Save the changes in the environment::

    tutor config save

Run the initialization script in your chosen environment (dev or local)::

    tutor [dev|local] do init -l ontask

Run the environment::

    tutor [dev|local] start -d

Get the OnTask URL::

    tutor config printvalue ONTASK_URL

Visit On Task landing page::

    http(s)://<ONTASK_URL>

.. image:: https://github.com/eduNEXT/tutor-contrib-ontask/assets/64440265/8c2949b2-c7a5-4608-8e52-9226986460c1

Then, login with your admin credentials -- you can find them in your ``config.yml``!

.. image:: https://github.com/eduNEXT/tutor-contrib-ontask/assets/64440265/18f1bbe1-dad1-43d2-9a64-3e8d88c1d8a2


Check out the `OnTask official documentation <https://ontask-version-b.readthedocs.io/>`__ for a detailed description of how to use it.

Configuration
-------------

The following configuration options are available for your ``config.yml``:

- ``ONTASK_DOCKER_IMAGE`` (default: ``docker.io/edunext/ontask:{{ ONTASK_VERSION }}``): OnTask production docker image to use.
- ``ONTASK_POSTGRES_DOCKER_IMAGE`` (default: ``postgres:14.12-bullseye``): Persistent layer docker image used by the current On Task APP version.
- ``ONTASK_APP_VERSION`` (default: ``Version_11_1``): On Task Django service version to be used when building a new On Task docker image,
- ``ONTASK_HOST`` (default: ``ontask.<LMS_HOST>``): Hostname for OnTask.
- ``ONTASK_PORT`` (default: ``80``): Port for OnTask.
- ``ONTASK_POSTGRES_HOST`` (default: ``postgres``): Hostname for the postgres service.
- ``ONTASK_DATABASE_URL`` (default: ``"postgres://{{ ONTASK_DB_USER }}:{{ ONTASK_DB_PASSWORD }}@postgres:5432/{{ ONTASK_DB_NAME }})"``: Connection string for postgres.
- ``ONTASK_REDIS_URL`` (default: "redis://{{ REDIS_HOST }}:{{ REDIS_PORT }}"): Connection string for redis.
- ``ONTASK_DB_NAME`` (default: ``ontask``): Database name for OnTask.
- ``ONTASK_DB_USER`` (default: ``ontask``): Database user for OnTask.
- ``ONTASK_DB_PASSWORD``: Database password for ``ONTASK_DB_USER``.
- ``ONTASK_POSTGRES_ROOT_USERNAME`` (default: ``postgres``): Username for root in the postgres service.
- ``ONTASK_POSTGRES_ROOT_PASSWORD``: Password for root in the postgres service.
- ``ONTASK_SUPERUSER_NAME`` (default: ``Admin``): Admin name for OnTask.
- ``ONTASK_SUPERUSER_EMAIL`` (default: ``admin@mail.com``): Admin email for OnTask.
- ``ONTASK_SUPERUSER_PASSWORD``: Admin password for OnTask.
- ``ONTASK_EXTRA_PRODUCTION_SETTINGS``: Extra Django configurations for production environments.
- ``ONTASK_EXTRA_DEV_SETTINGS``: Extra Django configurations for dev environments.
- ``ONTASK_EMAIL_ACTION_NOTIFICATION_SENDER`` (default: ``admin@mail.com``): Email used for notifications.
- ``RUN_ONTASK`` (default: ``true``): Whether to run On Task or not.
- ``RUN_POSTGRES`` (default: ``true``): Whether to run postgres or not.

The Django OnTask service hosting recommendations heavily inspired the templates used for this service but adapted for seamless integration
with Open edX. Here's the main difference:

- Supervisor is not used to privision celery and celery beat. Instead, only the Celery CLI is directly used as in other Open edX services.

License
-------

The code in this repository is licensed under the AGPL-3.0 unless otherwise noted.
