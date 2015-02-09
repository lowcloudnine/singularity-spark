# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from future.builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import sys
if sys.version_info.major == 2:
    # in Python 2 cPickle is much faster than pickle but doesn't deal w/ unicode
    import cPickle as pickle
else:
    # Python 3 loads the faster pickle by default if it's available
    import pickle

import random
import time

import initialize_spark
sc = initialize_spark.get_sc()

def obs_count(year):
    """ Returns the number of observations in a given year. """
    start_time = time.time()
    obs = sc.textFile("/user/schiefjm/weather/gsod/" + str(year))
    the_count = obs.count()
    end_time = time.time() - start_time

    # print("There were {:,} observations in {}.".format(the_count, year))
    # print("It took {:.2f} seconds to count them.".format(end_time))

    return year, the_count, round(end_time, 3)

def obs_count_test(num_tests, years):
    all_results = []
    for year in years:
        results = []
        for test in range(num_tests):
            results.append(obs_count(year))
        all_results.append(results)

    return all_results

def generate_test_results(all_results):
    print("Year\tObs\tTests\tMin\tMax\tAvg")
    print("*" * 45)
    for result in all_results:
        year = result[0][0]
        num_obs = result[0][1]
        num_tests = len(result)
        run_times = [test[2] for test in result]
        print("{}\t{:,}\t{}\t{:.2f}\t{:.2f}\t{:.2f}\t"\
              .format(year,
                      num_obs,
                      num_tests,
                      min(run_times),
                      max(run_times),
                      sum(run_times)/num_tests))

generate_test_results(obs_count_test(100, [1930, 1932, 1934, 1940, 1950]))

