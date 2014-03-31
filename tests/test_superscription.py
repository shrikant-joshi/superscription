#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_superscription
----------------------------------

Tests for `superscription` module.
"""

import os
import unittest
import pickle
import warnings

from superscription import Superscription


def fake_response(hub_mode, **kwargs):
    # Map path to the corresponding file
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    fpath =  os.path.join(BASE_DIR, 'tests/resources')
    resource_file =  '%s/%s_data' % (fpath, hub_mode)
    
    with open(resource_file, mode='rb') as f:
        text = f.read()

    response = pickle.loads(text)
    return response


class TestSuperscription(unittest.TestCase):

    def setUp(self):
        self.ss     = Superscription('demo', 'demo')
        self.assertIsNotNone(self.ss)

        self.ss._make_request = fake_response #fake out the method to ensure it return local pickled data.

        self.url    = 'http://push-pub.appspot.com/feed'
        self.cburl  = 'http://my.domain.tld/callback/'
        warnings.filterwarnings("error")


    def test_exceptions(self):
        with self.assertRaises(TypeError):
            self.ss.subscribe(self.url)

        with self.assertRaises(AttributeError):
            # self.ss._super_request("invalid hub mode", hub_topic=self.url)
            self.ss._construct_payload("invalid_mode", hub_topic=self.url)

        with self.assertRaises(AttributeError):
            # Check if at least one of password or token is passed
            Superscription('demo')


            # # The following tests fail - need to write proper code for this
            # # Invalid URLS do NOT return a 422 from Superfeedr
            # self.ss.subscribe("http://www.google") # pragma: no cover
            # self.ss.unsubscribe("http://www.google") # pragma: no cover

    def test_verify_url(self):
        # Check invalid URLs
        with self.assertRaises(AttributeError):
            self.ss._verify("http://google")
        with self.assertRaises(AttributeError):
            self.ss._verify("google.com")
        with self.assertRaises(AttributeError):
            self.ss._verify("invalid callback url")

    def test_make_request_returns_response(self):
        response = self.ss._make_request("subscribe", hub_topic=self.url, hub_callback=self.cburl)
        self.assertIsNotNone(response)
        self.assertIn(response.status_code, [200, 202, 204])    

    def test_payload_construction(self):
        # Check if valid hub_mode is provided
        with self.assertRaises(AttributeError):
            self.ss._construct_payload("invalid_mode", "json", hub_topic=self.url, hub_callback=self.cburl)
        with self.assertRaises(ValueError):
            self.ss._construct_payload("subscribe", "json", hub_topic=self.url, hub_callback=self.cburl, \
                                        hub_secret="RandomHubSecretForTesting", hub_verify="invalid")

        self.ss._construct_payload("subscribe", "json", hub_topic=self.url, hub_callback=self.cburl)
        # Check if valid RuntimeWarning is 'raised'
        with self.assertRaises(RuntimeWarning):
            payload = self.ss._construct_payload("subscribe", fmt="json", hub_topic=self.url, \
                                                hub_callback=self.cburl, foo="foo", bar="bar", baz="baz")

        payload = self.ss._construct_payload(hub_mode="subscribe", fmt="json", hub_topic=self.url, hub_callback=self.cburl)
        self.assertIsInstance(payload, dict)

    def test_subscribe(self):
        with self.assertRaises(UserWarning):
            result = self.ss.subscribe(self.url, self.cburl)
        result = self.ss.subscribe(self.url, self.cburl, hub_secret="RandomHubSecretForTesting")
        self.assertTrue(result)

        response = self.ss.response
        self.assertEqual(type(response).__name__, 'Response')
        self.assertEqual(response.status_code, 204)

    def test_list(self):
        result = self.ss.list(self.cburl)
        self.assertTrue(result)

        response = self.ss.response
        self.assertEqual(type(response).__name__, 'Response')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertEqual(data[0]['subscription']['feed']['url'], self.url)


    def test_retrieve(self):

        result = self.ss.retrieve(self.url)
        self.assertTrue(result)

        response = self.ss.response
        self.assertEqual(type(response).__name__, 'Response')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertIsNotNone(data.keys())
        self.assertEqual(data['status']['feed'], self.url)

    def test_unsubscribe(self):
        result = self.ss.unsubscribe(self.url, self.cburl)
        self.assertTrue(result)

        response = self.ss.response
        self.assertEqual(type(response).__name__, 'Response')
        self.assertEqual(response.status_code, 204)

    def tearDown(self):
        # self.patcher.start()
        warnings.resetwarnings()
