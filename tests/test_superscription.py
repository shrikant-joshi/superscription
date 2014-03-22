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

from superscription import superscription


def fake_response(hub_mode, **kwargs):
    # Map path to the corresponding file
    resource_file = os.path.normpath('tests/resources/%s_data' % hub_mode)
    
    with open(resource_file, mode='rb') as f:
        text = f.read()

    response = pickle.loads(text)
    return response


class TestSuperscription(unittest.TestCase):

    def setUp(self):
        self.ss     = superscription.Superscription('demo', 'demo')
        self.ss._make_request = fake_response #fake out the method to ensure it return local pickled data.

        self.url    = 'http://push-pub.appspot.com/feed'
        self.cburl  = 'http://my.domain.tld/callback/'


    def test_empty_args(self):
        with self.assertRaises(TypeError):
            self.ss.subscribe(self.url)
        
    def test_subscribe(self):
        result = self.ss.subscribe(self.url, self.cburl)
        self.assertTrue(result)

        response = self.ss.response
        # self.assertEqual(type(response).__name__, 'Response')
        self.assertEqual(response.status_code, 204)

    def test_list(self):
        result = self.ss.list(self.cburl)
        self.assertTrue(result)

        response = self.ss.response
        # self.assertEqual(type(response).__name__, 'Response')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertIsNotNone(data)
        self.assertEqual(data[0]['subscription']['feed']['url'], self.url)


    def test_retrieve(self):
        result = self.ss.retrieve(self.url)
        self.assertTrue(result)

        response = self.ss.response
        # self.assertEqual(type(response).__name__, 'Response')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.text)

        data = response.json()
        self.assertIsNotNone(data.keys())
        self.assertEqual(data['status']['feed'], self.url)

    def test_unsubscribe(self):
        result = self.ss.unsubscribe(self.url, self.cburl)
        self.assertTrue(result)

        response = self.ss.response
        # self.assertEqual(type(response).__name__, 'Response')
        self.assertEqual(response.status_code, 204)

    def tearDown(self):
        # self.patcher.start()
        pass


if __name__ == '__main__':
    unittest.main()