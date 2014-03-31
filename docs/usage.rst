========
Usage
========

Basic Usage
-----------

Basic usage is pretty straightforward and looks like this:

::

    >>> from superscription import Superscription
    >>> ss = Superscription("Marvin", "PainInMyDiodes")

You can also, pass in a token, instead of a password. In fact, it is
recommended!

::

    >>> ss = Superscription("Marvin", token="0123456789abcdef0123456789abcdef")

Don't worry, not passing either the password or the token will raise an
``AttributeError``!

::

    >>> ss = Superscription("ArthurDent")
    Traceback (most recent call last):
    [...]
    AttributeError: You must initialize the object with either a password or a token! We recommend the token for security purposes, as does Superfeedr!

Modes? Methods!
---------------

Each Superfeedr ``hub.mode`` (``subscribe``, ``unsubscribe``, ``list``,
``display``) is available as an object method of the Superscription
class. All parameters accepted by Superfeedr can be declared as keyword
arguments.

    NOTE: The order of the parameters is the same as specified in the
    `Superfeedr PuSH Webhooks
    documentation <http://documentation.superfeedr.com/subscribers.html#webhooks>`__,
    in case you want to pass them as ``args`` rather than ``kwargs``.
    Using keyword arguments is always recommended, though. :)

Paramters? Kwargs!
------------------

Any optional parameters allowed by the Superfeedr PuSH API can simply be
passed as keyword arguments for each of the corresponding method calls.
To construct the keyword argument corresponding to a parameter, replace
the dot (**.**) in the parameter name, with an underscore (**\_**).

For instance, ``hub.secret`` corresponds to ``hub_secret``:

::

    >>> ss = Superscription("demo", token="demo")
    >>> result = ss.subscribe(hub_topic='http://push-pub.appspot.com/feed', hub_callback="http://my.callback.tld/callback/", hub_verify="sync", hub_secret="RandomHubSecretGoesHere")
    >>> print result
    True

Parameters without a '.' in their name correspond to keyword arguments
with the same name. for instance, ``page`` can be passed as ``page``
itself:

::

    >>> result = ss.list(hub_callback="http://my.callback.tld/callback/", page="1")
    >>> print result
    True
    >>> ss.response.status_code
    202

\...except for the parameter ``format`` which corrresponds to the keyword
argument ``fmt``. This has been done deliberately, to avoid any
potential confusion/problems with the ``str.format()`` method/call.

Available methods
-----------------

All methods return a boolean ``True`` or ``False`` depending on whether
the subscription was successfully performed using Superfeedr or ran into
problems.

Potential problems have been documented (to some extent) in the section
`Errors & Warnings <#errors>`__.

Subscribe
~~~~~~~~~

The ``.subscribe()`` method takes TWO mandatory arguments, ``hub_topic``
& ``hub_callback``:

::

    >>> result = ss.subscribe('http://push-pub.appspot.com/feed', "http://my.domain.tld/callback/")
    >>> print result
    True
    >>> ss.response.status_code
    202

Unsubscribe
~~~~~~~~~~~

The ``.unsubscribe()`` method takes ONE mandatory argument,
``hub_topic``:

::

    >>> result = ss.unsubscribe(hub_topic='http://push-pub.appspot.com/feed')
    >>> print result
    True
    >>> ss.response.status_code
    202

If you have multiple subscriptions for the same ``hub_topic`` but each
one is associated with a different ``hub_callback``, you will have to
call the method each time for each (of the) callback(s) for which you
want to unsubscribe.

List
~~~~

The ``.list()`` method takes ONE mandatory argument, ``hub_callback``:

::

    >>> result = ss.list(hub_callback='http://my.domain.tld/callback')
    >>> print result
    True
    >>> ss.response.status_code
    200
    >>> ss.response.json()
    [{u'subscription': {u'feed': {u'url': u'http://push-pub.appspot.com/feed', u'title': u'Publisher example'}, u'secret': None, u'endpoint': u'http://my.domain.tld/callback', u'format': u'json'}}]

Retrieve
~~~~~~~~

The ``.retrieve()`` method takes ONE mandatory argument, ``hub_topic``:

::

    >>> result = ss.retrieve(hub_topic='http://push-pub.appspot,com/feed')
    >>> print result
    True
    >>> ss.response.status_code
    200
    >>> data = ss.response.json()
    >>> data.keys()
    [u'status', u'items', u'title']

Responses
---------

The response from Superfeedr is the standard ``Response`` object
returned by the \`\ ``requests`` module and is saved as an attribute on
the ``superscription`` object itself:

::

    >>> result = ss.subscribe('http://push-pub.appspot.com/feed', "http://my.domain.tld/callback/")
    >>> print ss.response
    <Response [204]>

Do note that the 'response' attribute is available on ``ss`` & not
``result``.

::

    >>> type(ss.response)
    requests.models.Response
    >>> ss.response.status_code
    204
    >>> ss.response.content
    ''
    >>> ss.response.text
    u''

Errors and Warnings
-------------------

If the Superfeedr request runs into problems, or is generally
unsuccessful for some reason, the execution is stopped by raising the
corresponding error.

Optional Arguments are, well, optional...
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Arguments with ``None`` values are discarded and a ``RuntimeWarning`` is
displayed before the API endpoint request is made:

::

    >>> result = ss.subscribe("http://push-pub.appspot.com/feed", "http://my.domain.tld/callback", hub_secret=None, hub_verify=None)
    [...]
    RuntimeWarning: Extra arguments passed in function call: hub_secret, hub_verify

Mandatory Arguments are MANDATORY!
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Not passing in the mandatory arguments raises the standard
``TypeError``:

::

    >>> result = ss.subscribe('http://push-pub.appspot.com/feed')
    [...]
    TypeError: subscribe() takes at least 3 arguments (2 given)

All URLs must be fully-qualified
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

URLs for ``hub_topic`` and ``hub_callback`` must be fully-qualified
URIs, with a minimum of ``scheme`` and ``hostname``, else you'll get an
``AttributeError`` on the first of them to be caught:

::

    >>> ss.subscribe("http://google", "my.domain.tld/callback")
    [...]
    AttributeError: http://google - URL is not fully-qualified!

--------------