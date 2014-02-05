.. python-cryptsy documentation master file, created by
   sphinx-quickstart on Sun Feb  2 19:15:37 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to python-cryptsy's documentation!
==========================================

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Cryptsy
===================
The cryptsy package provides a series of modules for working with the Cryptsy Web API.

.. automodule:: cryptsy

Bare API
===================
The bare_api module provides a series of methods for directly accessing the Cryptsy API. It does not do any kind of session management such as
storing application/private keys or rate-limiting the number of API calls that are made. All methods return raw JSON formatted data.

.. automodule:: cryptsy.bare_api
   :members: