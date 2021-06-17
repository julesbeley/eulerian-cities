# Cities - Eulerian Paths

This script returns the coordinates of a path which visits all the streets of a given city.

It relies on [OSMnx](https://github.com/gboeing/osmnx) to download and simplify the street network data and [networkx.algorithms.euler.eulerian_circuit](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.euler.eulerian_circuit.html) to produce the path. Users can provide a custom (lon,lat) starting point. The algorithm will find the closest OSM node from which to start the circuit. There is also an in-built method to save a .gpx file and/or a GIF animation of the Eulerian path, such as the one below. According to NetworkX, the eulerian_circuit method is a linear time implementation of the algorithm found [here](https://link.springer.com/article/10.1007/BF01580113). It may be difficult to calculate the Eulerian path for larger cities, and this script is best used for villages and small towns.

![alt text](Jonzieux.gif)
