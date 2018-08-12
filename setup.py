from setuptools import setup, find_packages

data_files = []

# Load README.md
with open("README.md", "r") as fp:
    long_desc = fp.read()

setup(
    name="python-twitch-irc",
    version="1.0.2",
    author="jspaulsen",
    author_email="jspaulsen@github.com",
    description="Python Library for Twitch IRC eccentricities",
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url='https://github.com/jspaulsen/python-twitch-irc',
    classifiers=(
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    packages=find_packages(),
    install_requires=[
      'pydle',
      'pendulum',
    ],
    data_files=data_files,
    entry_points={
      'console_scripts': [],
    },
)
