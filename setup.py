#!/usr/bin/env python
import os

from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(here, "pickydict", "__version__.py")) as f:
    exec(f.read(), version)

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    name="pickydict",
    version=version["__version__"],
    description="More picky version of Python dictionary.",
    long_description_content_type="text/markdown",
    long_description=readme,
    author="Florian Huber",
    author_email="",
    url="https://github.com/florian-huber/pickydict",
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    zip_safe=False,
    test_suite="tests",
    python_requires='>=3.6',
    install_requires=[],
    extras_require={"dev": ["prospector[with_pyroma]",
                            "pytest",
                            "pytest-cov",
                            ],
    }
)
