#!/usr/bin/env python3

from setuptools import setup

exec(compile(
    open('hstctl/info.py', 'r').read(),
    'hstctl/info.py', 'exec'
))

setup(
    name = 'hstctl',
    version = __version__,
    description = '',
    long_description = '',
    url = 'https://github.com/JanniKHv/hstctl',
    author = __author__,
    author_email = __email__,
    maintainer = __author__,
    maintainer_email = __email__,
    license = __license__,
    packages= ['hstctl'],
    scripts = ['bin/hstctl']
)