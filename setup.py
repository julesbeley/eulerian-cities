from setuptools import setup

setup(
    name='eulerian cities',
    author='Jules Beley',
    url='https://github.com/julesbeley/eulerian-cities',
    packages=['eulerian_cities'],
    python_requires=">=3.6",
    install_requires=[
        'networkx',
        'osmnx',
        'lxml'
    ]
)
