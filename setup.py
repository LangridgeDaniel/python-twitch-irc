from setuptools import setup, find_packages

data_files = []

setup(
    name='twitch_irc',
    version='0.1.0',
    description='',
    author='jpaulsen',
    url='https://github.com/jspaulsen/python-twitch-irc',
    packages=find_packages(),
    zip_safe=True,
    install_requires=[
      'pydle',
      'pendulum',
    ],
    data_files=data_files,
    entry_points={
      'console_scripts': [],
    },
)
