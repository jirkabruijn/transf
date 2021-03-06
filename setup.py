#!/usr/bin/env python

from setuptools import setup
exec(open('transf/version.py').read())

setup(
    name = 'transf',
    version=__version__,
    description = 'A test concerning transformations',
    url = 'https://github.com/jirkabruijn/transf.git',
    author = 'Jiri Bruijn',
    author_email = 'jirka.bruijn@gmail.com',
    license = 'unlicensed',
    packages=['transf'],
    zip_safe=False
)
