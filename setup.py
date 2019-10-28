#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'aio-pika',
    'aioredis',
    'Click>=7.0',
    'environs',
    'wcraas-common',
    'yarl>=1.3.0',
]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Kolokotronis Panagiotis",
    author_email='panagiks@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="WCraaS Storage Service",
    entry_points={
        'console_scripts': [
            'wcraas_control=wcraas_control.cli:main',
            'wcraas_list_collections=wcraas_control.cli:list_collections',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='wcraas_control',
    name='wcraas_control',
    packages=find_packages(include=['wcraas_control', 'wcraas_control.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/WCraaS/wcraas_control',
    version='0.1.2',
    zip_safe=False,
)
