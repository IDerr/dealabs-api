#!/usr/bin/env python
from setuptools import setup, find_packages

def install():
    desc = 'A Python client library for rutube!'
    setup(
        name='dealabs-api',
        version='0.1',
        description=desc,
        long_description=desc,
        author='IDerr',
        author_email='',
        url='https://github.com/IDerr/dealabs-api',
        classifiers=['Operating System :: POSIX',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: MacOS :: MacOS X',
                     'Programming Language :: Python',
                     'Programming Language :: Python :: 3.2',
                     'Programming Language :: Python :: 3.3',
                     'Programming Language :: Python :: 3.4',
                     'Programming Language :: Python :: 3.5',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3 :: Only'
                     ],
        packages=find_packages(),
        install_requires=[
            'requests',
            'requests_oauthlib'
        ],
    )

if __name__ == "__main__":
    install()
