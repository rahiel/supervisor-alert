#!/usr/bin/env python
from setuptools import setup

from supervisor_alert import __version__


try:
    import pypandoc
    import re
    long_description = pypandoc.convert("README.md", "rst")
    # remove raw html blocks, they're not supported on pypi
    long_description = re.sub("\s+\.\. raw:: html\s*.+? -->", "", long_description, count=2)
except:
    long_description = ""


setup(
    name="supervisor-alert",
    version=__version__,
    description="Receive notifications for supervisor process events",
    long_description=long_description,
    url="https://github.com/rahiel/supervisor-alert",
    license="Apache-2.0",

    py_modules=["supervisor_alert"],
    entry_points={"console_scripts": ["supervisor-alert=supervisor_alert:main"]},

    author="Rahiel Kasim",
    author_email="rahielkasim@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 2.7",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    keywords="supervisor alert event listener notify"
)
