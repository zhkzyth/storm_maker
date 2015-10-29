#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages


setup(
    name="project_name",
    version="1.0",
    packages=find_packages(exclude=["tests"]),
    url="http://url/to/project/location",
    author="author",
    author_email="author@email.com"
)
