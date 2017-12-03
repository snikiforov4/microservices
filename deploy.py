#!/usr/bin/python

import argparse
import os
import ConfigParser
import StringIO
import re
import subprocess

CUR_DIR = os.path.dirname(os.path.realpath(__file__)) 
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


if not ENV:
    props = read_property_file('.env')
    ENV = props['ENV']
    if not ENV:
        raise Exception('ENV variable not found in \'.env\' file')

s = raw_input('Do you want to deploy on %s? [y/N]' % ENV)
pattern = re.compile("^([yY][eE][sS]|[yY])+$")
if pattern.match(s):
    print("Deploy...")
    res = subprocess.check_output(['./deploy.sh', ENV], stderr=subprocess.STDOUT, cwd=CUR_DIR)
    print res

