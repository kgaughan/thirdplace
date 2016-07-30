#!/usr/bin/env python

import os.path

from setuptools import setup, find_packages


def read_files(filenames):
    here = os.path.abspath(os.path.dirname(__file__))
    for filename in filenames:
        with open(os.path.join(here, filename)) as f:
            yield f.read()


setup(
    name='thirdplace',
    version='0.0.1',
    description='thirdplace',
    long_description='\n\n'.join(read_files(['README', 'ChangeLog'])),
    url='-',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,

    install_requires=(
        'click==6.6',
        'Flask==0.11.1',
        'Flask-SQLAlchemy==2.1',
        'Flask-WTF==0.12',
    ),

    entry_points={
        'console_scripts': [
            'thirdplace-tool=thirdplace.tools:cli',
        ],
    },

    classifiers=(
        'Environment :: Other Environment',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ),

    author='Keith Gaughan',
    author_email='k@stereochro.me',
)
