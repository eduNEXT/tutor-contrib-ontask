Changelog
==========

..
   All enhancements and patches to openedx_events will be documented
   in this file.  It adheres to the structure of https://keepachangelog.com/ ,
   but in reStructuredText instead of Markdown (for ease of incorporation into
   Sphinx documentation and the PyPI description).

   This project adheres to Semantic Versioning (https://semver.org/).

.. There should always be an "Unreleased" section for changes pending release.


[18.0.0] - 2025-08-28
---------------------

Changed
=======

* Replaced usage of `pkg_resources` with `importlib.resources.files` for template loading.

BREAKING CHANGES
================

* This change drops support for Python <3.9, since `importlib.resources.files` is only available from 3.9 onwards.
