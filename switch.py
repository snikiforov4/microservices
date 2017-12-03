#!/usr/bin/python

import argparse
import os
import ConfigParser
import StringIO
import csv

PARSER = argparse.ArgumentParser(description='Process command line options.')
PARSER.add_argument("-e", "--env", help="environment name", default="")

ARGS = vars(PARSER.parse_args())
ENV = ARGS["env"]


def read_property_file(filename):
    with open(filename) as f:
        config = StringIO.StringIO()
        config.write('[dummy_section]\n')
        config.write(f.read())
        config.seek(0, os.SEEK_SET)

        cp = ConfigParser.RawConfigParser(allow_no_value=True)
        cp.optionxform = str
        cp.readfp(config)

        return dict(cp.items('dummy_section'))


def read_property_files(files):
    properties = {}
    for f in files:
        if os.path.isfile(f):
            properties.update(read_property_file(f))
    return properties


def write_properties(filename, dictionary):
    """ Writes the provided dictionary in key-sorted order to a properties file with each line of the format key=value

        :param filename    the name of the file to be written
        :param dictionary  a dictionary containing the key/value pairs.
    """
    open_kwargs = {'mode': 'w'}
    with open(filename, **open_kwargs) as csv_file:
        writer = csv.writer(csv_file, delimiter='=', escapechar='\\', quoting=csv.QUOTE_NONE)
        writer.writerows(dictionary.items())


# read properties firstly from default.env, then override it with env specific properties
files = ['default.env']
if ENV:
    files.append(ENV + '.env')
props = read_property_files(files)
write_properties('.env', props)

if ENV:
    print("Switched to %s" % ENV)
else:
    print("Switched to default env")
