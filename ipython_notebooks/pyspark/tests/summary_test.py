# -*- coding: utf-8 -*-

from __future__ import print_function

import time
import libs.initialize_spark
sc = libs.initialize_spark.get_sc()

import libs.header
the_header = libs.header.create_header(sc)

# Since Spark is being run local no need to specify a HDFS server.
def global_summary(year):
    """ Given a year will return a list of the mean temp, min temp, max temp
    and more as it expands.

    This will use one (hopefully) persistent RDD so it should be faster than
    using the individual functions above.

    """
    obs_rdd = sc.textFile("/user/schiefjm/weather/gsod/" + str(year))\
                         .filter(lambda line: "STN" not in line)
    num_obs = obs_rdd.count()

    sum_of_temps = obs_rdd.map(lambda line: float(line.split()[3]))\
                          .reduce(lambda x, y: x + y)
    mean_temp = round(sum_of_temps / num_obs, 2)

    max_temp = obs_rdd.map(lambda line: float(line.split()[17].strip("*")))\
                       .filter(lambda x: x < 160)\
                       .reduce(lambda x, y: x if x > y else y)
    min_temp = obs_rdd.map(lambda line: float(line.split()[18].strip("*")))\
                       .filter(lambda x: x != 999.9)\
                       .reduce(lambda x, y: x if x < y else y)

    return [year, mean_temp, min_temp, max_temp, num_obs]

def global_summary_test(num_tests, years):
    all_results = []
    for year in years:
        results = []
        for test in range(num_tests):
            start_time = time.time()
            year, mean_tmp, min_tmp, max_tmp, num_obs = global_summary(year)
            run_time = time.time() - start_time
            results.append([year, num_obs, mean_tmp, min_tmp, max_tmp, run_time])
        all_results.append(results)

    return all_results

def generate_test_results(all_results):
    print("Year\tObs\tTests\tMin\tMax\tAvg")
    print("*" * 45)
    for result in all_results:
        year = result[0][0]
        num_obs = result[0][1]
        num_tests = len(result)
        run_times = [test[-1] for test in result]
        print("{}\t{:,}\t{}\t{:.2f}\t{:.2f}\t{:.2f}\t"\
              .format(year,
                      num_obs,
                      num_tests,
                      min(run_times),
                      max(run_times),
                      sum(run_times)/num_tests))
    print("")

print(the_header)
generate_test_results(global_summary_test(10, [year for year in range(1929, 1940)]))

