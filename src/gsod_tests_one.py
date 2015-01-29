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

# ---- Initialize the sc variable for PySpark
import initialize_spark
sc = initialize_spark.get_sc()

# -------- Global Variables # bad should make a class
server_name = "hdfs://c2-master:8020/"
dir_name = "user/schiefjm/weather/gsod/"
data_source = server_name + dir_name

# ----------------------------------------------------------------------------
#    Functions 
# ----------------------------------------------------------------------------


def global_mean_temp(year):
    """ Calcuates the mean temperature from the mean temperature from all
    the observations for a given year from 1929 to 2009 inclusive. 

    """
    obs_rdd = sc.textFile(server_name + dir_name + str(year))
    num_obs = obs_rdd.filter(lambda line: "STN" not in line)\
                     .count()
    sum_mean_temps = obs_rdd.filter(lambda line: "STN" not in line)\
                            .map(lambda line: line.split()[3])\
                            .map(lambda value: float(value))\
                            .reduce(lambda x, y: x + y)
    return sum_mean_temps / num_obs, num_obs

def global_max_temp(year):
    """ Finds the maximum temperature from the maximum temperatuers from all
    the observations for a given year from 1929 to 2009 inclusive.
    
    """
    return sc.textFile(server_name + dir_name + str(year))\
                      .filter(lambda line: "STN" not in line)\
                      .map(lambda line: line.split()[17])\
                      .map(lambda value: float(value.strip("*")))\
                      .filter(lambda x: x < 150)\
                      .reduce(lambda x, y: x if x > y else y)

def global_min_temp(year):
    """ Finds the minimum temperature from the minimum temperatures from all
    the observations for a given year from 1929 to 2009 inclusive.
    
    """
    return sc.textFile(server_name + dir_name + str(year))\
                      .filter(lambda line: "STN" not in line)\
                      .map(lambda line: line.split()[18])\
                      .map(lambda value: float(value.strip("*")))\
                      .filter(lambda x: x != 999.9)\
                      .reduce(lambda x, y: x if x < y else y)

def global_summary(year):
    """ Given a year will return a list of the mean temp, min temp, max temp
    and more as it expands.

    This will use one (hopefully) persistent RDD so it should be faster than
    using the individual functions above.

    """
    obs_rdd = sc.textFile(server_name + dir_name + str(year))\
                         .filter(lambda line: "STN" not in line)
    num_obs = obs_rdd.count()

    sum_of_temps = obs_rdd.map(lambda line: float(line.split()[3]))\
                          .reduce(lambda x, y: x + y)
    mean_temp = sum_of_temps / num_obs

    max_temp = obs_rdd.map(lambda line: float(line.split()[17].strip("*")))\
                       .filter(lambda x: x < 160)\
                       .reduce(lambda x, y: x if x > y else y)
    min_temp = obs_rdd.map(lambda line: float(line.split()[18].strip("*")))\
                       .filter(lambda x: x != 999.9)\
                       .reduce(lambda x, y: x if x < y else y)
    
    return [year, mean_temp, min_temp, max_temp, num_obs]

# ----------------------------------------------------------------------------
#    Main 
# ----------------------------------------------------------------------------


def main():
    """ Run the script as a stand alone application. """
    start_year = 1929
    stop_year = 1929
    
    print("\n")
    # ---- Individual Functions 
    start = time.time()
    temperatures = [[year, 
                     global_mean_temp(year),
                     global_min_temp(year),
                     global_max_temp(year)] 
                       for year in xrange(start_year, stop_year + 1)] 
    
    for year, mean, min, max in temperatures:
        print("{}\t{:.1f}\t{:.1f}\t{:.1f}\t{}"\
                .format(year, mean[0], min, max, mean[1]))
    
    print("\nUsing individual functions took {} seconds."\
            .format(round(time.time() - start, 2)))
    
    print("\n")
    # ---- Single Function 
    start = time.time()
    temperatures = [global_summary(year) 
                       for year in range(start_year, stop_year + 1)] 
    
    for year, mean, min, max, num_obs in temperatures:
        print("{}\t{:.1f}\t{:.1f}\t{:.1f}\t{}"\
                .format(year, mean, min, max, num_obs))
    
    print("\nUsing a combined function took {} seconds."\
            .format(round(time.time() - start, 2)))

# ----------------------------------------------------------------------------
#    Name 
# ----------------------------------------------------------------------------


if __name__ == "__main__":
	main()
