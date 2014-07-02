#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()
from setuptools import setup, find_packages

setup(
    name = "herdsman",
    version = "0.1",
    packages = find_packages(),
    description = "Server for herding user's code running on the Student Robotics platform"
)
