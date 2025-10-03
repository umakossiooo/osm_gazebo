##############################################################################
#Author: Tashwin Khurana
#Version: 1.0
#Package: gazebo_osm
#
#Description: getOsmFile()
#             Downloads the .osm file for the stated bounding box and
#             Stores it in file with the specified name
##############################################################################

import urllib.request
import urllib.error
from lxml import etree


def getOsmFile(box, outputFile='map.osm', inputOsmFile=''):
    '''downloads the data file for the specified bounding box
       stores the file as outputFile, if inputOsmFile is not specified
       and also converts the data in the form of a dictionary'''
    if not box and not inputOsmFile:
        return None

    dataDict = {}
    if inputOsmFile:
        outputFile = inputOsmFile
    else:
        try:
            urlString = 'http://api.openstreetmap.org/api/0.6/map?bbox=' + str(box)[1:-1].replace(" ", "")
            print (urlString)
            osmFile = urllib.request.urlopen(urlString)
        except urllib.error.HTTPError:
            print ("\nError:\tPlease check the bounding box input arguments"
                   + "\n\tFormat: MinLon MinLat MaxLon MaxLat")
            return {}
        osm = open(outputFile, 'wb')

        osm.write(osmFile.read())

        osm.close()

    osmRead = open(outputFile, 'rb')

    try:
        root = etree.fromstring(osmRead.read())
        dataDict = []
        
        # Parse nodes
        for node in root.findall('node'):
            node_id = int(node.get('id'))
            node_data = {
                'id': node_id,
                'lat': float(node.get('lat')),
                'lon': float(node.get('lon')),
                'tag': {}
            }
            for tag in node.findall('tag'):
                node_data['tag'][tag.get('k')] = tag.get('v')
            
            dataDict.append({
                'type': 'node',
                'data': node_data
            })
        
        # Parse ways
        for way in root.findall('way'):
            way_id = int(way.get('id'))
            way_data = {
                'id': way_id,
                'nd': [int(nd.get('ref')) for nd in way.findall('nd')],
                'tag': {}
            }
            for tag in way.findall('tag'):
                way_data['tag'][tag.get('k')] = tag.get('v')
            
            dataDict.append({
                'type': 'way',
                'data': way_data
            })
        
        # Parse relations
        for relation in root.findall('relation'):
            rel_id = int(relation.get('id'))
            rel_data = {
                'id': rel_id,
                'member': [],
                'tag': {}
            }
            for member in relation.findall('member'):
                rel_data['member'].append({
                    'type': member.get('type'),
                    'ref': int(member.get('ref')),
                    'role': member.get('role', '')
                })
            for tag in relation.findall('tag'):
                rel_data['tag'][tag.get('k')] = tag.get('v')
            
            dataDict.append({
                'type': 'relation',
                'data': rel_data
            })
                
    except Exception as e:
        print(f"Error parsing OSM file: {e}")
        dataDict = []

    osmRead.close()

    return dataDict
