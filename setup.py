#!/usr/bin/env python

import os.path

from setuptools import setup, find_packages


def read_files(filenames):
    here = os.path.abspath(os.path.dirname(__file__))
    for filename in filenames:
        with open(os.path.join(here, filename)) as f:
            yield f.read()


setup(
    name="thirdplace",
    version="0.0.1",
    description="thirdplace",
    long_description="\n\n".join(read_files(["README", "ChangeLog"])),
    url="-",
    license="MIT",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=(
        "bbcode==1.0.24",
        "click==7.0",
        "Flask==1.1.1",
        "Flask-Security==3.0.0",
        "Flask-SQLAlchemy==2.4.1",
        "Flask-WTF==0.14.3",
    ),
    entry_points={"console_scripts": ["thirdplace-tool=thirdplace.tools:cli"]},
    classifiers=(
        "Environment :: Other Environment",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ),
    author="Keith Gaughan",
    author_email="k@stereochro.me",
)
