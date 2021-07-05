from lxml import etree



def trail_to_gpx(
    query,
    lon_lat_trail, 
    file_path,
):
    
    """
    Write the list of lon, lat coordinates to a 
    GPX (XML) file.
    """
    
    track = etree.Element('trk')
    doc = etree.ElementTree(track)
    segment = etree.SubElement(track, 'trkseg')

    for point in lon_lat_trail:
        lon, lat = point
        
        point = etree.SubElement(
            segment,
            'trkpt',
            lon=str(lon), 
            lat=str(lat)
        )

    tree = track.getroottree()
    
    if file_path is None:
        file_path = './' + query + '.gif'
    
    tree.write(
        file_path, 
        pretty_print=True,
        xml_declaration=True, 
        encoding='utf-8'
    )
