#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pkgversion import list_requirements, pep440_version, write_setup_py
from setuptools import find_packages

write_setup_py(
    name='fqn-decorators',
    version=pep440_version(),
    description="Easily create multi-purpose decorators that have access to the FQN of the original function.",
    long_description=open('README.rst').read(),
    author="Mattias Sluis",
    author_email='mattias.sluis@kpn.com',
    url='ssh://git@github.com:kpn-digital/py-fqn-decorators.git',
    install_requires=list_requirements('requirements/requirements-base.txt'),
    packages=find_packages(exclude=['decorators.tests*']),
    tests_require=['tox'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
