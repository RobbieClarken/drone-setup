from setuptools import setup
import re

with open('drone_setup/__init__.py') as file:
    version = re.search(r'__version__ = "(.*)"', file.read()).group(1)

setup(
    name='drone-setup',
    version=version,
    license='MIT',
    author='John Marcou',
    author_email='john.marcou@gmail.com',
    url='https://github.com/johnmarcou/drone-setup',
    packages=['drone_setup'],
    install_requires=[
        "pyaml",
        "click",
        "requests",
    ],
    entry_points={
        'console_scripts': ['drone-setup=drone_setup:main'],
    }
)
