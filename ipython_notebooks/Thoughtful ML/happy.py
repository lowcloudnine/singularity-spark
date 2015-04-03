#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Purpose
-------

A short script for calculating house happiness based on KNN.

"""
# ----------------------------------------------------------------------------
#    Imports
# ----------------------------------------------------------------------------

# ---- Future imports for Python 3 compatibility
from __future__ import print_function

# ---- Standard Libraries
import csv
import math
from random import randint

# ---- Scientific/Mathematical Libraries
import numpy as np

# ----------------------------------------------------------------------------
#    Functions
# ----------------------------------------------------------------------------


def read_values(file_name):
    """ Reads in the lat, lon and yes/no (1/0) from a csv file. """
    homes = []
    with open(file_name, 'rb') as csvfile:
        homes_reader = csv.reader(csvfile)
        for home in homes_reader:
            if "latitude" in home:
                continue
            location = np.array((float(home[0]), float(home[1])))
            rating = int(home[2])
            homes.append([location, rating])

    return homes

def absolute_happy(considered, homes):
    """ Given a considered home with a lat/lon numpy array and a list of homes
    in a list with a lat/lon numpy array and rating returns either happy or
    unhappy based on the value of the closest home in homes.

    """
    closest = []
    for home in homes:
        distance = np.linalg.norm(considered - home[0])
        closest.append([distance, home[1]])

    closest = sorted(closest)[0]
    happy = ""
    if closest[1] == 0:
        happy = "Not Happy"
    elif closest[1] == 1:
        happy = "Happy"

    return happy

def relative_happy(considered, homes):
    """ Given a considered home with a lat/lon numpy array and a list of homes
    in a list with a lat/lon numpy array and rating with a value of either 0
    or 1 returns an average of the top 10 if the number of homes is longer
    than 20 otherwise returns the top half of the length of homes.

    """
    closest = []
    for home in homes:
        distance = np.linalg.norm(considered - home[0])
        closest.append([distance, home[1]])

    closest = sorted(closest)

    if len(homes) >= 20:
        length = 10
    else:
        length = int(math.ceil(len(homes) / 2))

    closest = closest[:length]
    happy = 0
    for close in closest:
        happy += close[1]

    return round(float(happy/float(length)), 2)

def create_homes(data_file):
    """ Create a file of houses with ratings of 0 or 1. """
    with open(data_file, "w") as csvfile:
        ratings_writer = csv.writer(csvfile)
        ratings_writer.writerow(["latitude", "longitude", "rating"])
        for _i in range(100):
             lat = randint(0, 60)
             lon = randint(0, 60)
             rating = randint(0, 1)
             ratings_writer.writerow([lat, lon, rating])

# ----------------------------------------------------------------------------
#    Main
# ----------------------------------------------------------------------------


def main():
    """ Runs the script as a stand alone application. """
    data_file = "ratings.csv"
    create_homes(data_file)
    homes = read_values(data_file)

    houses = [np.array((x, x)) for x in range(10, 60, 10)]

    print("\nKNN")
    print("-" * 40)
    for house in houses:
        print("The house at: {} is {} by {}."\
              .format(house,
                      absolute_happy(house, homes),
                      relative_happy(house, homes)))

# ----------------------------------------------------------------------------
#    Name
# ----------------------------------------------------------------------------


if __name__ == "__main__":
    main()
