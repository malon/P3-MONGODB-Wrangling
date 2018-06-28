#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
from audit_fixme import is_reliable
from audit_cities import is_my_city
from audit_streets import get_street

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')



def shape_element(element):
    node = {}
    if (element.tag == "node" or element.tag == "way") :
        if is_reliable(element) and is_my_city(element, "vigo"):
            node['id'] = element.attrib.get('id') 
            node['type'] = element.tag 
            node['visible'] = element.attrib.get('visible') 
            node['created'] = {}
            node['created']['version'] = element.attrib.get('version')
            node['created']['changeset'] = element.attrib.get('changeset')
            node['created']['timestamp'] = element.attrib.get('timestamp')
            node['created']['user'] = element.attrib.get('user')
            node['created']['uid'] = element.attrib.get('uid')
            if element.tag == "node" :
                node['pos'] = [float(element.attrib.get('lat')), float(element.attrib.get('lon'))]
            if element.tag == "way" :
                node['node_refs'] = []
                for nd in element.iter('nd'):
                    node['node_refs'].append(nd.attrib['ref'])
            for tag in element.iter('tag'):
                if problemchars.search(tag.attrib['k']):
                    pass
                elif lower.search(tag.attrib['k']):
                    node[tag.attrib['k']] = tag.attrib['v']
                else:
                    m = lower_colon.search(tag.attrib['k'])
                    if m:
                        if len(m.group().split(":")) != 2 :
                            pass
                        elif m.group().split(":")[0] == "addr":
                            if "address" not in node.keys():
                                node['address'] = {}
                            if m.group().split(":")[1] == "street":
                                node['address']['street'] = get_street(element)
                            else:
                                node['address'][m.group().split(":")[1]] = tag.attrib['v']
                        else:
                            new = tag.attrib['k'].replace(":", "_")
                            node[new] = tag.attrib['v']
                    
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}10.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

data = process_map('vigo_box.osm', False)
pprint.pprint(data)
   