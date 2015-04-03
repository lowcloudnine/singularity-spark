#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Purpose
-------

To test counting larger data sets, i.e. over 1.5 million entities to count.

"""
# --------------------------------------------------------------------------------------
#    Imports
# --------------------------------------------------------------------------------------


# ---- Future: for easier porting to Python 3
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

try:
    from future.builtins import (bytes, str, open, super, range,
                                 zip, round, input, int, pow, object)
except:
    pass

# ---- Standard Libraries
import collections
import json
import random
import string
import time

# --- PySpark 
import pyspark
from pyspark import SparkConf
from pyspark import SparkContext

# ---- Custom Libraries and Utilities
from utils import header

# -------------------------------------------------------------------------------------
#    Functions
# -------------------------------------------------------------------------------------


def get_sc():
    """ Defines and returns a SparkContext from some configurations via SparkConf. """
    conf = SparkConf()
    conf.setAppName("Jon's PySpark")
    conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    conf.set("spark.kryroserializer.buffer.mb", "256")
    conf.set("spark.akka.frameSize", "500")
    conf.set("spark.akka.askTimeout", "30")
    
    return SparkContext(conf=conf)

def is_anagram(str_1, str_2):
    """ Given two (2) strings does a character count of each and returns if they are
    anagrams of each other.
    
    Returns a two value tuple with:
        * Result: a boolean
        * Size: integer of size of the strings or -1 if they are not the same size 
    
    """
    str_1 = "".join(str_1.split(" "))
    str_2 = "".join(str_2.split(" "))
    size_1 = len(str_1)
    size_2 = len(str_2)
    
    if size_1 != size_2:
        return False, -1
    
    str1 = sc.parallelize(str_1)
    cnt_str1 = str1.map(lambda w: (w, 1))\
                   .reduceByKey(lambda a, b: a + b)
    
    str2 = sc.parallelize(str_2)
    cnt_str2 = str2.map(lambda w: (w, 1))\
                   .reduceByKey(lambda a, b: a + b)
    
    return cnt_str1.collect() == cnt_str2.collect(), size_1
    
# -------------------------------------------------------------------------------------
#    Main
# -------------------------------------------------------------------------------------


def main():
    """ Runs the script as a stand alone application. """
    global sc
    sc = get_sc()
    print(header.create_header(sc))
    
    power = 5.6
    attempts = 1
    str_1 = string.digits * int(10**power)
    str_2 = str_1[::-1]
    print(len(str_1))
    print("{:>10}{:>8}{:>13}{:>11}"\
          .format("Attempt", "Result", "Size", "Run Time"))
    print("   " + "=" * 39)

    for i in range(attempts):
        start = time.time()
        result, size = is_anagram(str_1, str_2)
        print("{:>9}{:>9}{:>13}{:>11}"\
              .format("{:02}".format(i + 1), 
                      "True" if result else "False",
                      "{:,}".format(size),
                      (str(round(time.time() - start, 2))) + "s"))
    
# ------------------------------------------------------------------------------------
#    Name
# ------------------------------------------------------------------------------------


if __name__ == "__main__":
    main()