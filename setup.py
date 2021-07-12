from setuptools import setup

setup(
    name='eulerian cities',
    author='Jules Beley',
    url='https://github.com/julesbeley/eulerian-cities',
    packages=['eulerian_cities'],
    python_requires=">=3.6",
    install_requires=[
        'networkx>=2.5',
        'osmnx>=1.1',
        'geopandas>=0.9',
        'shapely>=1.7',
        'matplotlib>=3.3',
        'lxml>=4.6'
    ]
)
