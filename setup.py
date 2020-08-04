#!/usr/bin/env python3

from setuptools import setup

author = "lwzm"

setup(
    name="fsmhub",
    version="4.4",
    description="Finite State Machine storage hub",
    author=author,
    author_email="{}@qq.com".format(author),
    url="https://github.com/lwzm/fsmhub",
    keywords="fsm http web store".split(),
    packages=["fsmhub"],
    scripts=["fsm-step"],
    install_requires="pony fastapi uvicorn".split(),
    classifiers=[
        "Environment :: Console",
        "Programming Language :: Python :: 3",
    ],
)

# $ ./setup.py sdist bdist_wheel
# $ twine upload dist/fsmhub-xxx
