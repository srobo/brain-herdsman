#!/usr/bin/env python
import ez_setup
ez_setup.use_setuptools()

from setuptools import setup, find_packages


setup(
    name='sr.herdsman',
    version='0.1.0',
    packages=find_packages(),
    namespace_packages=['sr'],
    scripts=['bin/herdsman'],
    description="Server for herding user's code running on the Student "
                "Robotics platform",
    install_requires=[
        'autobahn >=0.10, <1',
        'PyYAML >=3.11, <4',
        'zope.interface >=4.1, <5',
        'Twisted >=15.4, <16',
        'sr.robot >= 0.1, <1',
    ],
)
