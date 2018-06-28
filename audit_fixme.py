#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict

def fixme_points(filename):
    dict = defaultdict(int)
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if (tag.attrib["k"] == "fixme"):
                    dict[tag.attrib["v"].lower().strip()] += 1
    return dict

def is_reliable(elem):
    for tag in elem.iter("tag"):
        if (tag.attrib["k"] != "fixme"):
            return True

def count_fixme_points(filename):
    result = {"fixme": 0,
            "reliable": 0
           }
    for event, elem in ET.iterparse(filename, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            found = False
            for tag in elem.iter("tag"):
                if (tag.attrib["k"] == "fixme"):
                    found = True
            if found:
                result["fixme"] += 1
            else:
                result["reliable"] += 1
    return result

if __name__ == "__main__":
    cities = fixme_points('vigo_box.osm')
    pprint.pprint(cities)
    result = count_fixme_points("vigo_box.osm")
    pprint.pprint(result)