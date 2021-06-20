# Cities - Eulerian Paths

This script returns the coordinates of a trail which visits all the streets of a given city (also known as an [Eulerian trail](https://en.wikipedia.org/wiki/Eulerian_path) in graph theory), based only on the city name. It provides support for Eulerian paths and circuits alike.

It relies on [OSMnx](https://github.com/gboeing/osmnx) to download and simplify the street network data and [NetworkX](https://github.com/networkx/networkx) to produce the path. Users can provide a custom (lon, lat) starting point. The algorithm will find the closest OSM node from which to start the path. There is also an built-in method to save a GPX file and/or a GIF animation of the Eulerian trail, such as the one below. 

<p align="center">
  <img src="Jonzieux_for_display.gif" width="800"/>
</p>

When users want an Eulerian circuit, the script eulerizes the street network using [nx.algorithms.euler.eulerize](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.euler.eulerize.html), after which it finds an Eulerian circuit using [nx.algorithms.euler.eulerian_circuit](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.euler.eulerian_circuit.html). According to NetworkX, the method is a linear time implementation of the algorithm found [here](https://link.springer.com/article/10.1007/BF01580113). In practice, users will probably find that the algorithm is too slow to find an Eulerian circuit for larger cities, and this script is best used for villages and small towns. 

When it comes to Eulerian paths, the script applies [nx.algorithms.euler.eulerian_path](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.euler.eulerian_path.html) to the raw street network, and raises an exception if the network has none. 
