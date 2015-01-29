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


def get_sc(app_name="My App", memory="2G", cores="32"):
    """  Returns a SparkContext with the configuration for a specific
    Spark Server.

    """
    conf = SparkConf()
    # conf.setMaster("spark://c2-master.ec2.internal:7077")
    conf.setAppName(app_name)
    # conf.set("spark.executor.memory", memory)
    # conf.set("spark.cores.max", cores)

    return SparkContext(conf=conf)
