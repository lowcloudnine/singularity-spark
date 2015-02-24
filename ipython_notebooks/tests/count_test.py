# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from future.builtins import (bytes, str, open, super, range,
                      zip, round, input, int, pow, object)

import cPickle as pickle
import random
import time

import libs.initialize_spark
sc = libs.initialize_spark.get_sc()

import libs.header
the_header = libs.header.create_header(sc)

def obs_count(year):
    """ Returns the number of observations in a given year. """
    start_time = time.time()
    obs = sc.textFile("/user/schiefjm/weather/gsod/" + str(year))
    obs = obs.filter(lambda line: "STN" not in line)
    the_count = obs.count()
    end_time = time.time() - start_time

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
    print()

print(the_header)
generate_test_results(obs_count_test(20, [year for year in range(1929, 1940)]))
generate_test_results(obs_count_test(10, [year for year in range(1940, 1950)]))
generate_test_results(obs_count_test(5, [year for year in range(1950, 1960)]))
generate_test_results(obs_count_test(2, [year for year in range(1960, 1970)]))
generate_test_results(obs_count_test(2, [year for year in range(1970, 1980)]))
generate_test_results(obs_count_test(1, [year for year in range(1980, 1990)]))
generate_test_results(obs_count_test(1, [year for year in range(1990, 2000)]))
generate_test_results(obs_count_test(1, [year for year in range(2000, 2010)]))

