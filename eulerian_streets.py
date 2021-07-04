import networkx as nx
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Point, LineString
from animate import animate_from_trail
from GPX import lon_lat_trail_to_gpx



def get_source_node(
    start_lon_lat,
    original_edge_gdf,
    original_node_gdf
):
    """
    Return closest OSM node in street network, when a 
    custom lon,lat starting point is provided by user.
    """
    
    start_point = Point(start_lon_lat)
    start_lon_lat_series = gpd.GeoSeries([start_point])

    start_lon_lat_gdf = gpd.GeoDataFrame(
        geometry=start_lon_lat_series,
        crs=original_edge_gdf.crs
    )

    start_lon_lat_gdf = ox.project_gdf(start_lon_lat_gdf)
    projected_nodes = ox.project_gdf(original_node_gdf)

    start_geom = start_lon_lat_gdf.geometry.iloc[0]
    geoms = projected_nodes.geometry

    distances = geoms.apply(lambda x: x.distance(start_geom))
    source = distances.idxmin()
    
    return source
    
# separate OSM_ID trail to lat/lon trail as function
# add "quiet" argument for saving only
    
def eulerian_trail_from_place(
    query,
    query_type='place',
    network_type='all_private',
    trail_type='circuit',
    start_lon_lat=None,
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
    
    if start_lon_lat is not None:
        source = get_source_node(
            start_lon_lat,
            original_edges,
            original_nodes
        )
        
    else:
        source = None
    
    if trail_type == 'path':
        if nx.has_eulerian_path(city):
            trail = list(nx.eulerian_path(city,source=source))
            
        else:
            raise nx.NetworkXError('Graph has no Eulerian paths.')
            
    if trail_type == 'circuit':      
        if not nx.is_eulerian(city):
            city = nx.eulerize(city)

        trail = list(nx.eulerian_circuit(city,source=source))
            
    origin_id = trail[0][0]
    origin_node = original_nodes.loc[origin_id]
    lon_lat_trail = [(origin_node.x, origin_node.y)]
    
    index = original_edges.index
    step_dic = {edge:0 for edge in trail}
    
    for edge in trail:
        is_edge = [set(edge).issubset(i) for i in index]  
        gdf_edges = original_edges[is_edge]
        
        geom = gdf_edges.geometry   
        step = step_dic[edge]
        
        coords = list(geom.iloc[step].coords)

        test_order = lon_lat_trail[-1] == coords[0]  
        order = 1 if test_order else -1
        lon_lat_trail.extend(coords[::order])

        n_edges = len(gdf_edges)

        if n_edges > 1:
            step_dic[edge] = (step + 1) % n_edges
            
    if save_trail_as_gpx == True:
        lon_lat_trail_to_gpx(
            query,
            lon_lat_trail, 
            gpx_fp,
        )
        
    if save_animation == True:
        animate_from_trail(
            query,
            lon_lat_trail,
            original_edges,
            animation_fp,
            animation_fig_size,
            animation_frame_share,
            animation_dpi
        )
                    
    lon_lat_trail = LineString(lon_lat_trail)
    
    return lon_lat_trail
