"""
A lightweight library for serialization of arbitrary Python objects into dicts.
"""

import re
from setuptools import setup

def find_version(fname):
    """
    Attempts to find the version number in the file names fname.
    Raises RuntimeError if not found.
    """
    version = ""
    with open(fname, "r") as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError("Cannot find version information")
    return version


setup(
    name="beerializer",
    author="Alexander Pushkov",
    author_email="alexander@notpushk.in",
    url="https://beerializer.songbee.net/",
    version=find_version("beerializer/__init__.py"),
    description=__doc__.replace("\n", " ").strip(),
    long_description=open("README.rst").read(),
    keywords=[
        "serialization", "rest", "json", "api", "marshal",
        "marshalling", "deserialization", "validation", "schema"
    ],
    packages=["beerializer"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Software Development",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ]
)
