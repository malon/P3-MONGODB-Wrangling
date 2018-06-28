# P3-MONGODB-Wrangling

Contents:

* ProjectNotes (ypynb, html, pdf): contains the notes of the wrangling process and the answers to the rubric questions.
* audit_cities.py: script to audit the cities of the datapoints in order to filter out only the one we are interested in.
* audit_fixme.py: script to audit the fixme tags, read its content and drop them
* audit_streets.py : script to audit the street types, cleaning and homogenizing them
* data_process.py: script to read the xml file from OSM
* link_map: link to the map represented by the downloaded OSM dataset



NOTES: 
* the code is using the original file vigo_box.osm, from which the included file sample_vigo.osm is just a sample. 
* some of the functions used in the scripts were taken from the Udacity´s MongoDB course case study exercises.