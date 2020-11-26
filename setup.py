#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()


setup(
    name="fqn-decorators",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Easily create multi-purpose decorators that have access to the FQN of the original function.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Mattias Sluis",
    author_email="mattias.sluis@kpn.com",
    url="https://github.com/kpn-digital/py-fqn-decorators",
    packages=find_packages(exclude=["tests*"]),
    tests_require=["tox"],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
