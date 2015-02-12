# -*- coding: utf-8 -*-
"""
Purpose
-------

A centralized file for initializing 'sc' for using in Python programs that
run on the Spark Server.

"""
# ----------------------------------------------------------------------------
#    Imports
# ----------------------------------------------------------------------------


# ---- PySpark Library
import pyspark
from pyspark import SparkConf
from pyspark import SparkContext

# ----------------------------------------------------------------------------
#    Functions
# ----------------------------------------------------------------------------


def get_sc():
    """  Returns a SparkContext with the configuration for a specific
    Spark Server.

    """
    return SparkContext(conf=SparkConf())
