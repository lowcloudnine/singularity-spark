# -*- coding: utf-8 -*-
"""
Purpose
-------

A centralized file for generating header information for tests.

"""
# ----------------------------------------------------------------------------
#    Imports
# ----------------------------------------------------------------------------


import datetime
import inspect
import platform

# ----------------------------------------------------------------------------
#    Functions
# ----------------------------------------------------------------------------


def sparkcontext_info(sc):
    """ Returns a string of the SparkContext info """
    settings = []

    settings.append("\nSpark Configuration\n")
    settings.append("=" * 72 + "\n")
    for name, value in sc._conf.getAll():
        if len(value) > 68:
            value = value[:32] + " .. " + value[-32:]
        settings.append("{:}\n    {}\n".format(name, value))
    settings.append("=" * 72 + "\n")

    return "".join(settings)

def create_header(sc):
    """  Returns a string of header info for print by a test script. """
    # Get the file name of the calling file, this is the test name
    frame = inspect.stack()[1]
    module = str(inspect.getmodule(frame[0]))
    file_name = (module.split("/")[-1])[:-2]
    file_name = ("{:<15} {:>25}".format("Test Name", file_name))

    # Get the date time for the time the script was started
    date = datetime.datetime.now().strftime("%d %b %Y")
    time = datetime.datetime.now().strftime("%H:%M:%S")

    date_str = "{:<15} {:>25}".format("Date", date)
    time_str = "{:<15} {:>25}".format("Start Time", time)

    # Get the name of the machine the script is running on
    machine = "{:<15} {:>25}".format("Machine", platform.node())

    # Get the SparkContext information and display it
    spark_context = sparkcontext_info(sc)

    values = ["",
              file_name,
              machine,
              date_str,
              time_str,
              spark_context,
              ""]

    header = "\n".join(values)
    return header
