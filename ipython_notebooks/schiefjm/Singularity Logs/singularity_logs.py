# -*- coding: utf-8 -*-
"""
Purpose
-------

A specialized class for managing an Elasticsearch index for a small sample of 
Singularity logs given in a JSON format.

"""
# -----------------------------------------------------------------------------
#    Imports
# -----------------------------------------------------------------------------


from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from future.builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

# ---- Standard Libraries not included in pylab
import collections
import csv
import json
import os
import string
import sys

# ---- Scientific Libraries
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy as sp

# ---- GeoSpatial Libraries
import shapely
import shapely.wkt

# ---- Extra Libraries for additional functionality
import elasticsearch
from elasticsearch import Elasticsearch

# -----------------------------------------------------------------------------
#    Class:  SingularityLogs
# -----------------------------------------------------------------------------


class SingularityLogs(object):
    """ A class that simplifies the creation, deletion and manipulation of an
    Elasticsearch index for some singularity log entries.
    
    """
    def __init__(self, index_name=None):
        self.index_name = index_name
        self.es = Elasticsearch(['http://search-01.ec2.internal:9200'])

    def create_index(self):
#        create_body = json.dumps({
#            "mappings": {
#                "log_entry": {
#                    "properties": {
#                        "data": {
#                            "properties": {
#                                "point": { "type": "geo_point" },
#                                "RSV_IP_ADDRESS": { "type": "ip", "store": "true" },
#                                "destIP": { "type": "ip", "store": "true" },
#                                "BBOX_WKT": { "type": "geo_shape" },
#                                "BBOX_WKT2": { "type": "geo_shape" }
#                            }
#                        }
#                    }
#                }
#            }
#        })
        
        try:
            result = self.es.indices.create(
                index = self.index_name,
                # body = create_body
            )
        except:
            result = "Error:  {}".format(sys.exc_info())
            # result = "Index already exists. {}".format(e)
        
        return result

    def delete_index(self):
        try:
            result = self.es.indices.delete(index=self.index_name)
        except:
            result = "Index does not exist, can't delete."
        
        return result

    def insert_log_entry(self, entry):
        # create a raw field of the data as string
        entry['data_raw'] = json.dumps(entry['data'])
        entry['data_raw'] = entry['data_raw'].replace('"', '\'')
        
        # if RSV_IP_ADDRESS is a key then convert it to an ip address
        # if the address starts with a number
        try:
            ip = entry['data']['RSV_IP_ADDRESS']
            entry['data']['RSV_IP_ADDRESS'] = ip.replace("X", "0")
        except:
            pass
        try:
            ip = entry['data']['destIP']
            entry['data']['destIP'] = ip.replace("X", "0")
        except:
            pass
        
        # look for WKT geoshapes
        for key, value in entry['data'].items():
            try:
                start = (value.split(" "))[0]
                if start in ['POINT', 'LINESTRING', 'POLYGON', 
                             'MULTIPOINT', 'MULTILINESTRING', 'MULTIPOLYGON']:
                    value = self._wkt2geo(value)
                    coords = value['coordinates']
                    entry['data'][key] = coords
            except:
                pass
            
        result = self.es.index(index=self.index_name,
                          doc_type="log_entry",
                          body=entry)
        return result
    
    def _wkt2geo(self, wkt):
        """ Converts a WKT string into a GeoJSON string. """
        # using Shapely   
        polyshape = shapely.wkt.loads(wkt)
        return shapely.geometry.mapping(polyshape)
    
    def show_mapping(self):
        return self.es.indices.get_mapping(index=self.index_name)
    
    def count(self):
        return self.es.count(self.index_name)