#!/usr/bin/env python

from setuptools import setup
exec(open('transf/version.py').read())

REQUIRES = ['setuptools',
            'numpy',
            'math',
            'functools']
setup(
    name = 'transf',
    version='0.0.1',
    description = 'A test concerning transformations',
    url = 'https://github.com/jirkabruijn/transf.git',
    author = 'Jiri Bruijn',
    author_email = 'jirka.bruijn@gmail.com',
    license = 'unlicensed',
    packages=['transf'],
    zip_safe=False,
    install_requires=REQUIRES
)
