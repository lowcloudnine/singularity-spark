# -*- coding: utf-8 -*-
""" 
Purpose
-------

A class for searching and counting on the GSOD data in Elasticsearch.

"""
# -----------------------------------------------------------------------------
#    Imports
# -----------------------------------------------------------------------------


from __future__ import absolute_import
from __future__ import print_function

import datetime
import json
import requests
import sys

# -----------------------------------------------------------------------------
#    Class:  ESGsod
# -----------------------------------------------------------------------------


class ESGsod(object):
    """ Interacts with Elasicseach for interacting with Global Summary of the
    Day (GSOD) weather data.  Will act on a specific index only.
    
    """
    def __init__(self, 
                 server_address="http://search-01.ec2.internal:9200/", 
                 index="gsod"):
        self.address = server_address
        self.index = index
        query_type = "_search"
        
        query = json.dumps({
            "query": {
                "match": { 
                    "Mean Temp": "50.0"
                }
            },
            "size": "1"
        })
        
        try:
            response = requests.get(self.address + self.index + query_type, data=query)
        except:
            print("Unable to connect to Elasticsearch server please make sure" + \
                  "you have the right information entered correctly.\n")
            sys.exit(1)
            
        self.uri = self.address + self.index
        
    def search(self, 
               num_of_obs=1, 
               parameter=None):
        """ Given a number for observations returns them based on the parameter.  If
        the parameter is None will return all the parameters, i.e. the entire 
        observation document.
        
        """
        uri = self.uri + "/_search/"
        
        if parameter == None:
            query = json.dumps({
                "query": {
                    "filtered": {
                        "query": {
                            "match_all": {}
                        }
                    }
                },
                "size": num_of_obs })
        else:
           query = json.dumps({
                "query": {
                    "filtered": {
                        "query": {
                            "match_all": {}
                        }
                    }
                },
                "_source": parameter,
                "size": num_of_obs }) 
        
        response = requests.get(uri, data=query)
        return json.loads(response.text)
    
    @staticmethod
    def str2date(a_date):
        """ Given a string representing a date in the form YYYY-MM-DD returns 
        a date object with the given date.
        
        """
        the_date = a_date.split("-")
        
        year = int(the_date[0])
        month = int(the_date[1])
        day = int(the_date[2])
        
        return datetime.date(year, month, day)   
    
    def search_by_date(self, 
                       start_date, 
                       end_date, 
                       num_of_obs=1, 
                       parameter=None):
        """ Given a date range with a start and end date in the format of 
        YYYY-MM-DD returns json of the resulting search from Elasticsearch with a
        GSOD index on it.
        
        """
        uri = self.uri + "/_search/"
        start_date = (self.str2date(start_date)).isoformat()
        end_date = (self.str2date(end_date)).isoformat()
                                  
        if parameter == None:
            query = json.dumps({
                "query": {
                     "filtered": {
                         "filter": {
                             "range": {
                                 "Date": {
                                     "gte": start_date,
                                     "lte": end_date
                                 }
                             }
                         }
                     }
                 },
                 "size": num_of_obs
             })
        else:
           query = json.dumps({
                "query": {
                     "filtered": {
                         "filter": {
                             "range": {
                                 "Date": {
                                     "gte": start_date,
                                     "lte": end_date
                                 }
                             }
                         }
                     }
                 },
                 "_source": parameter,
                 "size": num_of_obs
             })
        
        response = requests.get(uri, data=query)
        return json.loads(response.text)