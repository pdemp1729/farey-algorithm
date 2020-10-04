from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="farey_algorithm",
    version="0.2",
    description="Implementation of best-rational-approximation algorithms.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pdemp1729/farey_algorithm",
    author="Paul Dempster",
    author_email="pdempster2@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    license="MIT",
    packages=find_packages(exclude=("*.tests",)),
    python_requires=">=3.6",
    extras_require={
        "formatting": ["black", "flake8"],
        "testing": ["pytest"],
        "coverage": ["pytest-cov"],
    },
    zip_safe=False,
)
