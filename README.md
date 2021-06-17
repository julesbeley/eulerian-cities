# Cities - Eulerian Paths

This script returns the coordinates of a path which visits all the streets of a given city.

This work relies on [OSMnx](https://github.com/gboeing/osmnx) to download and simplify the street network data and [networkx.algorithms.euler.eulerian_circuit](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.euler.eulerian_circuit.html) to produce the path. Users can provide a custom (lon,lat) starting point. The algorithm will find the closest OSM node from which to start the circuit. There is also an in-built method to save a .gpx file and/or a GIF animation of the Eulerian path, such as the one below.

![alt text](Jonzieux.gif)
