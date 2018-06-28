#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict
from audit_fixme import is_reliable

from audit_fixme import is_reliable

def is_my_city(elem, city):
    for tag in elem.iter("tag"):
        if ((tag.attrib["k"] == "addr:city") or
            (tag.attrib["k"] == "is_in:city") or
            (tag.attrib["k"] == "is_in:municipality")):
            if (city == tag.attrib["v"].lower()):
                return True
    return False         
    
def city_names(filename):
    dict = defaultdict(int)
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            if is_reliable(elem):
                for tag in elem.iter("tag"):
                    if (tag.attrib["k"] == "addr:city"):
                        dict[tag.attrib["v"]] += 1
    return dict

if __name__ == "__main__":
    cities = city_names('vigo_box.osm')
    pprint.pprint(cities)