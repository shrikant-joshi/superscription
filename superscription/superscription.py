#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Superscriptions
~~~~~~~~~~~~~~~
Superscriptions is a (very) thin wrapper around the Superfeedr PubSubHubbub API, using the excellent requests library by Kenneth Reitz.

What it does:

    * Encapsulates the HTTP request generation for all four PuSH methods: 'subscribe' 'unsubscribe' 'list' and 'retrieve'
    * Evaluates the response from the Superfeedr API 
    * Return `True` or `False` representing success and failure, respectively

Response from the Superfeeder PuSH API is a standard `requests.Response` object and made available under the `response` attribute.

What it doesn't do:
    * Anything else, really.

What do YOU want it to do?
    * Let me know. Raise an issue. Fork and submit a PR. :)

:copyright: (c) 2014 Shrikant Joshi
:license: BSD, See LICENSE for more details.
"""

import warnings
import urlparse
import requests

from requests import auth


SUPERFEEDR_API_URL  = "https://push.superfeedr.com"
ALLOWED_MODES       = {
                        'subscribe'     : requests.post, 
                        'unsubscribe'   : requests.post, 
                        'list'          : requests.get, 
                        'retrieve'      : requests.get,
                    }
ALLOWED_PARAMS      = {
                        "hub_topic"     : "hub.topic", 
                        "hub_callback"  : "hub.callback", 
                        "hub_secret"    : "hub.secret", 
                        "hub_verify"    : "hub.verify", 
                        "page"          : "page", 
                        "retrieve"      : "retrieve", 
                        "count"         : "count", 
                        "before"        : "before", 
                        "after"         : "after",
                        "fmt"           : "format",
                    }

class Superscription(object):
    """A super-thin wrapper around the Superfeedr PuSH API. Documentation at:
        http://documentation.superfeedr.com/

    This object encapsulates the basic API endpoints available for PuSH subscriptions
    # TODO: The `track` endpoint. 

    Usage:
    >>> superscription = Superscription(username='demo', password='demo')
    """

    def __init__(self, username, password=None, token=None):
        """Initialize a Superscription object.

        Superfeedr API authentication requires a username and either a :param string password: or a :param string token:. The :param string token: method is recommended. 

        You can create an account at:
            http://www.superfeedr.com/subscriber

        :param string username: Superfeedr username.
        :param string password: If using password authentication, Superfeedr password
        :param string token: If using token authentication, Superfeedr token. Generate a token from the "Authentication Tokens" ection of your Dashboard.
        .. versionadded:: 0.1.0
        """
        if not password and not token:
            raise AttributeError("You must initialize the object with either a password or a token! We recommend the token for security purposes, as does Superfeedr!")
        self.password       = password
        self.token          = token
        self.username       = username


    def _construct_payload(self, hub_mode, fmt="json", **kwargs):
        """Validate & construct the payload for the superscription request"""

        if hub_mode not in ALLOWED_MODES:
            raise AttributeError("hub_mode must be one of: %s" % str(ALLOWED_MODES.keys()))


        payload = {
            'format'        : fmt,
            'hub.mode'      : hub_mode,
        }

        hub_verify = kwargs.get("hub_verify", None)
        if hub_verify and hub_verify not in ["sync", "async"]:
            raise ValueError("If defined, hub_verify can only accept 'sync' or 'async' as values!")

        for key, value in kwargs.items():
            if value and key in ALLOWED_PARAMS:
                pkey = ALLOWED_PARAMS[key]
                payload[pkey] = kwargs.pop(key)

        if kwargs:
            warn_msg = "Extra arguments passed in function call: %s" % ", ".join(kwargs.keys())
            warnings.warn(warn_msg, RuntimeWarning)

        return payload


    def _make_request(self, hub_mode, **kwargs): # pragma: no cover
        """POST the superscription request using ``requests`` module. Return evaluated response.

        :param string api_call: should be a bound method, extracted from `ALLOWED_MODES`
        :param string payload: constructed `ALLOWED_PARAMS`

        """
        api_call = ALLOWED_MODES.get(hub_mode, None)
        if not api_call:
            raise ValueError("Invalid value for hub_mode; allowed modes are: %s" % ", ".join(ALLOWED_MODES.keys()))

        payload         = self._construct_payload(hub_mode=hub_mode, **kwargs)
        response        = api_call( SUPERFEEDR_API_URL, 
                                    params=payload, 
                                    auth=auth.HTTPBasicAuth(self.username, self.password), 
                                    # headers={'Accept': 'application/json'}
                            )
        return response
        
    def _super_request(self, hub_mode, **kwargs):
        """The base method for all requests sent to superfeedr. 

        Returns a boolean True/False of the response received from Superfeedr:        
            - True for HTTP-2XX status-codes
            - False for non-2XX status-codes
        In addition, this method raises all exceptions generated by the ``requests`` module, if any.

        :param string hub_mode: MUST be one of the `ALLOWED_MODES`

        After the request succeeds, the response atrribute of the current object is populated with the 
        `response` generated by the ``requests` module

        :param string response: The response, if any is made available as an object attribute on the 
        current object for later processing, if required.
        """

        self.hub_mode   = hub_mode
        self.response   = response = self._make_request(hub_mode, **kwargs)

        if response.status_code in [200, 202, 204]:
            result = True
        else: # pragma: no cover
            result = False
            response.raise_for_status()
        return result


    def _verify(self, hub_topic):
        """Simple validation of URLs before sending to Superfeedr"""

        parsed_url  = urlparse.urlparse(hub_topic)

        unqualified_uri   = None in (parsed_url.scheme, parsed_url.hostname)
        invalid_hostname  = not parsed_url.hostname or "." not in parsed_url.hostname

        if unqualified_uri or invalid_hostname:
            raise AttributeError("The URL %s is not fully-qualified!" % hub_topic)
        return hub_topic


    def subscribe(self, hub_topic, hub_callback, hub_secret=None, hub_verify=None, retrieve=None):
        """Set up a superfeedr subscription ('superscription') for a feed.

        REQUIRED:
        :param string hub_topic: The feed url subscribed with Superfeedr, for which you want the past entries.
        :param string hub_callback: The URL to which notifications will be sent. Make sure you it’s web-accessible, i.e. not behind a firewall.
        OPTIONAL:
        :param string hub_secret: [RECOMMENDED] A unique secret string which will be used by us to compute a signature. You should check this signature when getting notifications.
        :param string hub_verify: Accepts either the string-value `sync` or `async` and informs Superfeedr to perform a PubSubHubbub verification of the subscribe intent synschronously or asynschronously.
        :param string fmt: `json` if you want to retrieve entries in json format (for feeds only!). You can also use an `Accept` HTTP header like this: `Accept: application/json`
        :param string retrieve: If set to 'true', the response will include the current representation of the feed as stored in Superfeedr, in the format desired. Please check the Schema for more details:

        Schema: http://documentation.superfeedr.com/schema.html

        Usage:
        >>> from superscription import Superscription
        >>> ss = Superscription(username='demo', password='demo')
        >>> ss.subscribe('http://push-pub.appspot.com/feed', 'http://my.domain.tld/callback', hub_secret='RandomHubSecret')
        True
        >>> print ss.response
        <Response [204]>
        >>> print type(ss.response)
        <class 'requests.models.Response'>
        >>> print ss.response.status_code
        204
        """
        if not hub_secret:
            warnings.warn("You are strongly recommended to set a hub secret on a per-feed basis!", UserWarning)

        self.hub_topic  = self._verify(hub_topic)
        hub_callback    = self._verify(hub_callback)
        
        kwargs          = dict(hub_topic=hub_topic, hub_callback=hub_callback, hub_secret=hub_secret, hub_verify=hub_verify)

        return self._super_request(hub_mode="subscribe", **kwargs)


    def list(self, hub_callback, page=None):
        """List feeds associated with the specified callback URL.

        REQUIRED:
        :param string hub_callback: The callback url with which you subscribed and for which you want to find subscriptions. It can include % as a wildcard.
        OPTIONAL:
        :param string page: If there are more than 20 matching subscriptions, you may want to paginate over them. First page (default) is 1.

        Usage:
        >>> from superscription import Superscription
        >>> ss = Superscription(username='demo', password='demo')
        >>> ss.list('http://my.domain.tld/callback')
        True
        >>> print ss.response
        <Response [200]>
        >>> print type(ss.response)
        <class 'requests.models.Response'>
        >>> print ss.response.status_code
        200
        """
        kwargs      = dict(hub_callback=hub_callback, page=page)

        return self._super_request(hub_mode="list", **kwargs)


    def retrieve(self, hub_topic, count=None, before=None, after=None, fmt=None, callback=None):
        """Retrieve entries for a subscribed feed.

        REQUIRED:
        :param string hub_topic: The feed url subscribed with Superfeedr, for which you want the past entries.
        OPTIONAL:
        :param int count: The number of items to retrieve. Current max is 50 and default is 10.
        :param int before: The `id` of an entry in the feed. The response will only include entries published before this one.
        :param int after: The `id` of an entry in the feed. The response will only include entries published after this one.
        :param string fmt: `json` if you want to retrieve entries in json format (for feeds only!). You can also use an `Accept` HTTP header like this: `Accept: application/json`
        :param string fmt: (only if you’re using the JSON format) This will render the entries as a JSONP. 


        Usage:
        >>> from superscription import Superscription
        >>> ss = Superscription(username='demo', password='demo')
        >>> ss.retrieve('http://push-pub.appspot.com/feed')
        True
        >>> print ss.response
        <Response [200]>
        >>> print type(ss.response)
        <class 'requests.models.Response'>
        >>> print ss.response.status_code
        200
        """

        kwargs          = dict(hub_topic=hub_topic, count=count, before=before, after=after, fmt=fmt, callback=callback)
        if fmt and fmt is not "json": # pragma: no cover
            warnings.warn("callbacks are supported only for JSON. Ignoring callback...")
            callback = None
        return self._super_request(hub_mode="retrieve", **kwargs)


    def unsubscribe(self, hub_topic, hub_callback=None, hub_secret=None, hub_verify=None):
        """Unset an existing 'superscription' for a feed from Superfeedr.

        REQUIRED:
        :param string hub_topic: The feed url subscribed with Superfeedr, which you want to unsubscribe.
        OPTIONAL:
        :param string hub_callback: The URL to which notifications will be sent. It is optional if you are only subscribed to the feed 'once', with a single `hub.callback`. If you have multiple subscriptions, you will need to supply the `hub.callback` parameter. It is also required if you use the `hub.verify` param.
        :param string hub_verify: `sync` or `async`. Superfeedr will perform a PubSubHubbub verification of the unsubscribe intent synschronously or asynschronously.


        Usage:
        >>> from superscription import Superscription
        >>> ss = Superscription(username='demo', password='demo')
        >>> ss.unsubscribe('http://push-pub.appspot.com/feed', 'http://my.domain.tld/callback')
        True
        >>> print ss.response
        <Response [204]>
        >>> print type(ss.response)
        <class 'requests.models.Response'>
        >>> print ss.response.status_code
        204
        """
        self.hub_topic  = self._verify(hub_topic)
        if hub_callback:
            hub_callback    = self._verify(hub_callback)
        kwargs          = dict(hub_topic=hub_topic, hub_callback=hub_callback, hub_secret=hub_secret, hub_verify=hub_verify)

        return self._super_request(hub_mode="unsubscribe", **kwargs)
