import osmnx as ox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from shapely.geometry import Point
import geopandas as gpd



def animate_from_trail(
    query,
    lat_lng_trail,
    original_edges,
    file_path,
    fig_size,
    frame_share,
    dpi
):
    """
    Create GIF animation of trail from lat,lng coordinates. Projects 
    the points in the trail to UTM and uses the GeoDataFrame.plot() method 
    to plot the background edges.
    """
    
    points = [Point(list(reversed(p))) for p in lat_lng_trail]
    series = gpd.GeoSeries(points)

    gdf = gpd.GeoDataFrame(geometry=series,
                           crs=original_edges.crs)
    
    gdf = ox.project_gdf(gdf)

    increment = int(1/frame_share)
    
    x, y = gdf.geometry.x, gdf.geometry.y
    x, y = x.tolist(), y.tolist()
    x, y = x[::increment], y[::increment]
    
    plt.ioff()
    
    fig, ax = plt.subplots(figsize=(fig_size, fig_size))

    for key, spine in ax.spines.items():
        spine.set_visible(False)

    ax.tick_params(left=False, 
                   bottom=False)
    
    ax.tick_params(labelleft=False, 
                   labelbottom=False)

    p = 200
    
    ax.set_xlim([min(x)-p, max(x)+p])
    ax.set_ylim([min(y)-p, max(y)+p])

    bg_edges = ox.project_gdf(original_edges)
    
    bg_edges.plot(
        ax=ax, 
        color='black', 
        alpha=0.5,
        lw=1/5*fig_size
    )

    point, = ax.plot(
        [], 
        [], 
        color='red',
        marker='o',
        ms=4/5*fig_size
    )
    
    line, = ax.plot(
        [], 
        [], 
        color='red', 
        alpha=0.2, 
        lw=4/5*fig_size
    )

    
    def animate(i):
        point.set_data(x[i], y[i])
        line.set_data(x[:i], y[:i])
        return point, line

    
    animation = FuncAnimation(
        fig=ax.figure, 
        func=animate, 
        frames=len(x), 
        interval=50, 
        blit=True
    )
    
    fps = 40*frame_share
    
    if file_path is None:
        file_path = './' + query + '.gif'
           
    animation.save(
        filename=file_path, 
        dpi=dpi, 
        fps=fps
    )
