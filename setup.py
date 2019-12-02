#!/usr/bin/env python3

from setuptools import setup

author = "lwzm"
name = "fsm-hub"

setup(
    name=name,
    version="2.0",
    description="Finite State Machine storage hub",
    author=author,
    author_email="{}@qq.com".format(author),
    url="https://github.com/{}/{}".format(author, name),
    keywords="fsm http web store".split(),
    packages=["fsm_hub"],
    scripts=[name, "fsm-step"],
    install_requires="pony pyyaml falcon requests".split(),
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
    ],
)
