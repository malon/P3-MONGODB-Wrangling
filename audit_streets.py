#!/usr/bin/env python
# -*- coding: utf-8 -*-


import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
from audit_fixme import is_reliable
from audit_cities import is_my_city

OSMFILE = "vigo_box.osm"
street_type_re = re.compile(r'^\S+\.?\b', re.IGNORECASE)


expected = [u"rua", u"avenida", u"camiño", u"praza", u"lugar", u"estrada", u"caleixon", u"poligono", u"area", u"paseo"]

mapping = { u"avda": "avenida",
            u"calle": "rua",
            u"cl" : "rua",
            u"carretera" : "estrada",
            u"ctra" : "estrada",
            u"calleja/callejón" : "caleixon",
            u"plaza" : "praza",
            u"praza/patio" : "praza/patio",
            u"C/Alcalde" : "rua alcalde"
           }

def delete_accents(word):
    return word.replace(u"á", u"a").replace(u"é", u"e").replace(u"í", u"i").replace(u"ó", u"o").replace(u"ú", u"u")

def get_street(elem):
    city = None
    for tag in elem.iter("tag"):
        if (tag.attrib["k"] == "addr:street"):
            street = delete_accents(tag.attrib["v"].lower().strip())
            m = street_type_re.search(street)
            if m:
                street_type = m.group()
            if street_type in expected:
                return street
            elif street_type in mapping.keys():
                street = street.replace(street_type, mapping[street_type])
                return street
            else:
                return "rua "+street
    return city   

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            if (is_reliable(elem) and is_my_city(elem, "vigo")):
                for tag in elem.iter("tag"):
                    if is_street_name(tag):
                        audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

if __name__ == "__main__":
    st_types = audit(OSMFILE)
    pprint.pprint(dict(st_types))