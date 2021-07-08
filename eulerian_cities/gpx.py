from lxml import etree



def trail_to_gpx(
    query,
    lat_lng_trail, 
    file_path,
):
    
    """
    Write the list of lat,lng coordinates to a GPX (XML) file.
    """
    
    track = etree.Element('trk')
    doc = etree.ElementTree(track)
    segment = etree.SubElement(track, 'trkseg')

    for point in lat_lng_trail:
        lat, lng = point
        
        point = etree.SubElement(
            segment,
            'trkpt',
            lon=str(lng), 
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
