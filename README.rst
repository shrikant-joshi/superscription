===============================
Superscription
===============================

.. image:: https://badge.fury.io/py/superscription.png
    :target: http://badge.fury.io/py/superscription
    
.. image:: https://travis-ci.org/shrikant-joshi/superscription.png?branch=master
        :target: https://travis-ci.org/shrikant-joshi/superscription

.. image:: https://pypip.in/d/superscription/badge.png
        :target: https://crate.io/packages/superscription?version=latest


Superscriptions: A (super-)thin Python2.7 wrapper around the Superfeedr PubSubHubbub API.

It uses the excellent ``requests`` module by Kenneth Reitz for
interacting with the Superfeedr API endpoints. As a result, all
responses are available (as object attributes on the ``superscription`` object itself) 
in their entirety, should you choose to introspect and/or work with them further.

-  Free software: BSD license
-  Documentation: http://superscription.rtfd.org.

Features
--------

1. The various ``hub.mode``\ s offered by Superfeedr are made available
   as straightforward & intuitive methods.
2. An (almost) one-to-one mapping of allowed parameters to
   keyword-arguments for these methods.
3. Each response is available in its entirety for inspection if needed,
   thanks to Kenneth Reitz's excellent ``requests`` module.


Basic Usage
-----------

Basic usage is pretty straightforward and looks like this:

::

    >>> from superscription import Superscription
    >>> ss = Superscription("Marvin", "PainInMyDiodes")

More examples and details available in the `documentation <http://superscription.readthedocs.org>`_!

Please feel free to add to/modify the documentation and the
project by forking and submitting a PR.