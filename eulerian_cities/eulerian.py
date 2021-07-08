import networkx as nx
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point, LineString
from eulerian_cities import animate
from eulerian_cities import gpx



def get_source_node(
    start,
    original_edge_gdf,
    original_node_gdf
):
    """
    Return closest OSM node in street network, when a custom starting point
    (lat,lng or address) is provided by user.
    """
    
    if isinstance(start,str):
        start = ox.geocoder.geocode(query=start)
    
    start_point = Point(list(reversed(start)))
    start_lng_lat_series = gpd.GeoSeries([start_point])

    start_lng_lat_gdf = gpd.GeoDataFrame(
        geometry=start_lng_lat_series,
        crs=original_edge_gdf.crs
    )

    start_lng_lat_gdf = ox.project_gdf(start_lng_lat_gdf)
    projected_nodes = ox.project_gdf(original_node_gdf)

    start_geom = start_lng_lat_gdf.geometry.iloc[0]
    geoms = projected_nodes.geometry

    distances = geoms.apply(lambda x: x.distance(start_geom))
    source = distances.idxmin()
    
    return source
    
    
def id_trail_to_lat_lng_trail(
    id_trail,
    original_nodes,
    original_edges
):
    """
    Convert list of OSM_ID tuples to list of coordinates. When several 
    edges connect two nodes, make sure each edge is visited at least once. 
    """
    
    origin_id = id_trail[0][0]
    origin_node = original_nodes.loc[origin_id]
    
    lat_lng_trail = [(origin_node.y, origin_node.x)]
    
    index = original_edges.index
    step_dic = {edge: 0 for edge in id_trail}
    
    for edge in id_trail:
        is_edge = [set(edge).issubset(i) for i in index]  
        gdf_edges = original_edges[is_edge]
        
        geom = gdf_edges.geometry   
        step = step_dic[edge]
        
        coords = list(geom.iloc[step].coords)
        coords = [list(reversed(point)) for point in coords]

        reverse = lat_lng_trail[-1] != coords[0]
        
        if reverse:
            coords = reversed(coords)
            
        lat_lng_trail.extend(coords)
        n_edges = len(gdf_edges)

        if n_edges > 1:
            step_dic[edge] = (step + 1) % n_edges
        
    return lat_lng_trail

    
def eulerian_trail_from_place(
    query,
    quiet=False,
    query_type='place',
    network_type='walk',
    trail_type='circuit',
    start=None,
    save_trail_as_gpx=False,
    gpx_fp=None,
    save_animation=False,
    animation_fp=None,
    animation_fig_size=5,
    animation_frame_share=1,
    animation_dpi=80
):
    """
    Return Eulerian circuit or path as LineString, from city name, bounding box,
    or (address, dist) tuple. Queries are passed to ox.graph.graph_from_place, 
    ox.graph.graph_from_bbox, or ox.graph.graph_from_address. If the query is a 
    place name, it must be geocodable and have polygon boundaries. If the query
    is a bounding box, it must be in (north, south, east, west) format. If
    the query is an address, it must take the form (address, dist) with
    dist the distance from the address within which nodes will be retained.
    """
    
    if query_type == 'place':
        city = ox.graph.graph_from_place(
            query, 
            network_type=network_type
        )
        
    elif query_type == 'bbox':
        city = ox.graph.graph_from_bbox(
            *query, 
            network_type=network_type
        )
    
    elif query_type == 'address':
        city = ox.graph.graph_from_address(
            *query, 
            network_type=network_type
        )
    
    city = city.to_undirected()
    original_nodes, original_edges = ox.graph_to_gdfs(city)
    
    if start is not None:
        source = get_source_node(
            start,
            original_edges,
            original_nodes
        )
        
    else:
        source = None
    
    if trail_type == 'path':
        if nx.has_eulerian_path(city):
            id_trail = list(nx.eulerian_path(city,source=source))
            
        else:
            raise nx.NetworkXError('Graph has no Eulerian paths.')
            
    if trail_type == 'circuit':      
        if not nx.is_eulerian(city):
            city = nx.eulerize(city)

        id_trail = list(nx.eulerian_circuit(city,source=source))
        
    lat_lng_trail = id_trail_to_lat_lng_trail(
        id_trail,
        original_nodes,
        original_edges
    )
            
    if save_trail_as_gpx == True:
        gpx.trail_to_gpx(
            query,
            lat_lng_trail, 
            gpx_fp,
        )
        
    if save_animation == True:
        animate.animate_from_trail(
            query,
            lat_lng_trail,
            original_edges,
            animation_fp,
            animation_fig_size,
            animation_frame_share,
            animation_dpi
        )
                    
    lng_lat_trail = [list(reversed(p)) for p in lat_lng_trail]
    lng_lat_trail = LineString(lng_lat_trail)
    
    if not quiet:
        return lat_lng_trail
    