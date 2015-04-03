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
    the_sum = 0
    for arg in sys.argv[1:]: # sys.argv[0] is the name of the script
        the_sum += int(arg)
        
    return the_sum 

def main():
    """ Runs the script as a stand alone application. """
    # print(use_argparse())
    print(use_sys_args())

# -----------------------------------------------------------------------------
# Name
# -----------------------------------------------------------------------------


if __name__ == "__main__":
    main()