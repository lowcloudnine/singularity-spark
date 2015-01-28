# -*- coding: utf-8 -*-
""" 
Purpose
-------

Use spark-submit to load weather gsod files and see if I can play with the
output.

"""
# ----------------------------------------------------------------------------
#    Imports
# ----------------------------------------------------------------------------


# ---- Future Functions
from __future__ import print_function

# ---- Standard Libraries
import csv
import StringIO
import time

# ---- PySpark Libraries
import pyspark
from pyspark import SparkConf
from pyspark import SparkContext

# sc defined global as there can be only one
# -- there needs to be a better way to do this
sc = SparkContext(conf=SparkConf())

# ----------------------------------------------------------------------------
#    Functions 
# ----------------------------------------------------------------------------


def global_mean_temp(year):
    """ Calcuates the mean temperature from the mean temperature from all
    the observations for a given year from 1929 to 2009 inclusive. 

    """
    server_name = "hdfs://c2-master:8020/"
    dir_name = "user/schiefjm/weather/gsod/"
    year_name = str(year)

    obs_rdd = sc.textFile(server_name + dir_name + year_name)
    num_obs = obs_rdd.count()
    sum_mean_temps = obs_rdd.filter(lambda line: "STN" not in line)\
                            .map(lambda line: line.split()[3])\
                            .map(lambda value: float(value))\
                            .reduce(lambda x, y: x + y)
    return round(sum_mean_temps / num_obs, 2)

# ----------------------------------------------------------------------------
#    Main 
# ----------------------------------------------------------------------------


def main():
    """ Run the script as a stand alone application. """
    # ---- First Decade 
    start = time.time() 
    mean_temps = [[year, global_mean_temp(year)] 
                    for year in xrange(1929, 1939 + 1)] 
    for mean_temp in mean_temps:
        print("{}:  {}".format(mean_temp[0], mean_temp[1])) 
    
    print("\nFirst decade took: {} seconds.".format(round(time.time() - start, 2)))

    # ---- Last Year
    start = time.time()
    year = 2009
    mean_temp = global_mean_temp(year)
    print("{}:  {}".format(year, mean_temp)) 
    
    print("\nLast Year took: {} seconds.".format(round(time.time() - start, 2)))

# ----------------------------------------------------------------------------
#    Name 
# ----------------------------------------------------------------------------


if __name__ == "__main__":
	main()
