#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" 
Purpose
-------

Problem 19 from http://anandology.com/python-practice-book/getting-started.html

"""
# -----------------------------------------------------------------------------
# Imports
# -----------------------------------------------------------------------------


from __future__ import print_function

import argparse
import sys

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------


def use_argparse():
    """ Parse the command line arguments using argparse. """
    parser = argparse.ArgumentParser(description='Add some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+', 
                        help='integers to sum')
    parser.add_argument('-s', '--sum', dest='accumulate', action='store_const', 
                        const=sum, default=sum,
                        help='sum the integers')
    
    args = parser.parse_args()
    return args.accumulate(args.integers)

def use_sys_args():
    """ Parse the command line arguments using sys.args. """
    # There are 2 possible ways to achieve the result in one line.
    # One using a map:
    # return sum(list(map(int, sys.argv[1:])))
    # or using a list comprehension.
    return sum([int(i) for i in sys.argv[1:]])

    # per http://stackoverflow.com/questions/1247486/python-list-comprehension-vs-map
    # list comprehesion is considered more pythonic but if lambdas are not used then
    # map will be microscopically faster.

def main():
    """ Runs the script as a stand alone application. """
    # print(use_argparse())
    print(use_sys_args())

# -----------------------------------------------------------------------------
# Name
# -----------------------------------------------------------------------------


if __name__ == "__main__":
    main()