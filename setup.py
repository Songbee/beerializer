"""
Package to convert arbitrary python objects into DTOs ready
for serialization and validation.
"""

__version__ = "0.1.0"

from setuptools import setup


setup(
    name="beerializer",
    author="Songbee Team",
    author_email="hi@songbee.net",
    url="https://github.com/Songbee/beerializer",
    version=__version__,
    description=__doc__,
    setup_requires=["setuptools-markdown"],
    long_description_markdown_filename="README.md",
    keywords="dto serializer serialize REST marshal JSON",
    packages=["beerializer"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: Public Domain",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
        "Topic :: Software Development",
    ]
)
