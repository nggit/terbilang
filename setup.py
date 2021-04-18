#!/usr/bin/env python

from setuptools import setup

with open('README.md') as fh:
    long_description = fh.read()

setup(
    name='terbilang',
    packages=['terbilang'],
    version='0.0.5',
    license='MIT',
    author='nggit',
    author_email='contact@anggit.com',
    description='Python Terbilang',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nggit/terbilang',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
