#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='superscription',
    version='0.1.1',
    description='Superscriptions: A (super-)thin Python2.7 wrapper around the Superfeedr PubSubHubbub API.',
    long_description=readme + '\n\n' + history,
    author='Shrikant Joshi',
    author_email='shrikant.j@gmail.com',
    url='https://github.com/shrikant-joshi/superscription',
    packages=[
        'superscription',
    ],
    package_dir={'superscription': 'superscription'},
    include_package_data=True,
    install_requires=[
        'requests'
    ],
    license="BSD",
    zip_safe=False,
    keywords='superscription',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
    test_suite='tests',
)