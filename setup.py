#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

package_dir = {
    'citation_rabbot': 'citation_rabbot',
    'citation_rabbot.jumps': 'citation_rabbot/jumps'
}

setup(
    name='citation-rabbot',
    version='3.10.1',
    author='yindaheng98',
    author_email='yindaheng98@gmail.com',
    url='https://github.com/yindaheng98/citation-rabbot',
    description=u'A telegram bot jumping in your citation database like a rabbit!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_dir=package_dir,
    packages=[key for key in package_dir],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'python-telegram-bot>=20.7',
        'neo4j>=5.15.0'
    ],
)
