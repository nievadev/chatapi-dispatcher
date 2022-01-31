======================
Dispatcher of Messages
======================
------------------------------------------------------------------------------
A microservice that sanitizes, verifies requests and provides precise feedback
------------------------------------------------------------------------------

Introduction
============

This is a project made at work, of which the .git folder has been removed to delete
any records of sensible information (like credentials) of the past, that way this
doesn't violate any conditions!
The responsibility of this microservice is to comply to a standard, named and defined
*MessageDTO* (specified with the help of *Pydantic* in src/schemas/message_dto.py), so a
certain number of fields is expected in an exact way. These fields are looked up into the
POSTed request's body to the */v1/messages* endpoint.

Development Technologies Used
=============================

- Docker
- Pipenv
- Unittest
- Pytest
- Make

Deployment
==========

Production
----------
::

    $ docker image build --tag testing:1 .
    $ docker container run --publish 8001:8001 --rm -it testing:1

Development
-----------

This command will start a local development server.

::

    $ make dev

Usage
=====

Tests
-----
::

    $ make tests

Coverage
--------
::

    $ make coverage

Code-check
----------

There's a make statement that uses mypy, flake8, and pylint. This project is entirely typed
and mypy compliant.

::

    $ make check

Documentation
-------------

Go to **localhost:8001/docs** and you will see plenty of examples to test out!

This project is fully documented and 100% test-covered.
