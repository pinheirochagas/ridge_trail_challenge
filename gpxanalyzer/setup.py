from setuptools import setup, find_packages

setup(
    name='gpxanalyzer',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'gpxpy',
        'matplotlib'
    ],
)