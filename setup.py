from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="signalwire-swml",
    version="1.22",
    author="Brian West",
    author_email="brian@signalwire.com",
    description="A Python package for generating SignalWire Markup Language (SWML)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/briankwest/signalwire-swml",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyyaml>=5.1",
    ],
) 