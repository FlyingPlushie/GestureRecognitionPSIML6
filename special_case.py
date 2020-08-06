from xml.dom import minidom
import os
import xmltodict
from typing import List

f = open("FPS\KinectOutput182\Skeleton\Skeleton 77.xml") 
skeleton_xml = f.read()
skeleton_xml_parsed = xmltodict.parse(skeleton_xml)

if 'Joints' in skeleton_xml_parsed['ArrayOfSkeleton']['Skeleton'][0]:
    print("yes")