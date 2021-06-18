# Cities - Eulerian Paths

This script returns the coordinates of a path which visits all the streets of a given city (also known as an [Eulerian path](https://en.wikipedia.org/wiki/Eulerian_path) in graph theory), based only on the city name.

It relies on [OSMnx](https://github.com/gboeing/osmnx) to download and simplify the street network data and [Networkx](https://github.com/networkx/networkx) to produce the path. Users can provide a custom (lon,lat) starting point. The algorithm will find the closest OSM node from which to start the path. There is also an in-built method to save a .gpx file and/or a GIF animation of the Eulerian path, such as the one below. 

<p align="center">
  <img src="Jonzieux.gif" width="800"/>
</p>
  
The algorithm makes the street network Eulerian using [networkx.algorithms.euler.eulerize](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.euler.eulerize.html), after which it finds a Eulerian path using [networkx.algorithms.euler.eulerian_circuit](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.euler.eulerian_circuit.html). According to NetworkX, the method is a linear time implementation of the algorithm found [here](https://link.springer.com/article/10.1007/BF01580113). In practice, users will probably find that the algorithm is too slow to find an Eulerian path for larger cities, and this script is best used for villages and small towns.
