# coding=utf-8
from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="OctoPrint-EnclosureHeaterCommand",
    version="0.1.3",
    description="OctoPrint plugin to process custom enclosure heater commands and send JSON API requests.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Greg Schroeder",
    author_email="gregwschroeder@gmail.com",
    url="https://github.com/gregwschroeder/OctoPrint-EnclosureHeaterCommand",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "OctoPrint>=1.4.0",
        "requests"
    ],
    license="AGPLv3",
    classifiers=[
        "Framework :: OctoPrint",
        "License :: OSI Approved :: GNU Affero General Public License v3 (AGPLv3)",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        "octoprint.plugin": [
            "EnclosureHeaterCommand = octoprint_EnclosureHeaterCommand"
        ]
    }
)
