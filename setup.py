#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

readme = open('README.md').read()
doclink = """
Documentation
-------------

The full documentation is at http://omnithumb.rtfd.org."""
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='omnithumb',
    version='0.1.0',
    description='Mostly stateless microservice for generating on-the-fly thumbs and previews of a wide variety of file types.',
    long_description=readme + '\n\n' + doclink + '\n\n' + history,
    author='michaelb',
    author_email='michaelpb@gmail.com',
    url='https://github.com/michaelpb/omnithumb',
    packages=[
        'omnithumb',
    ],
    package_dir={'omnithumb': 'omnithumb'},
    include_package_data=True,
    install_requires=[
    ],
    license='MIT',
    zip_safe=False,
    keywords='omnithumb',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
)
