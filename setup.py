#!/usr/bin/env python3

from setuptools import setup


exec(compile(
    open('hstctl/info.py', 'r').read(),
    'hstctl/info.py', 'exec'
))

DESCRIPTION = '/etc/hosts file manager'
LONG_DESCRIPTION = 'Hstctl lets you easily manage and structure your /etc/hosts file'

setup(
    name = 'hstctl',
    version = __version__,
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    url = 'https://github.com/JannikHv/hstctl',
    author = __author__,
    author_email = __email__,
    maintainer = __author__,
    maintainer_email = __email__,
    license = __license__,
    packages= ['hstctl'],
    scripts = ['bin/hstctl']
)
