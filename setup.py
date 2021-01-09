#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
    name = "herdsman",
    version = "0.1",
    packages = find_packages(),
    scripts = ["bin/herdsman"],
    description = "Server for herding user's code running on the Student Robotics platform",
    install_requires = ["autobahn == 0.8.13",
                        "pyudev == 0.15",
                        "pyyaml == 3.13",
                        "zope.interface == 4.1.1",
                        "Twisted == 14.0.0" ],
)
