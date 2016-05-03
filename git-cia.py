#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import argparse
import subprocess

parser = argparse.ArgumentParser(description= 'Git: add files and then commit\n' +
                                 'It expands to the following git commands: \n' +
                                 ' git add ... ; git commit ...',
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('-m', dest="message", help='message')
parser.add_argument('files', nargs='*', help='files to commit')
opts = parser.parse_args()

if opts.files:
    status = subprocess.call(["git", "add"] + opts.files)
else:
    status = subprocess.call(["git", "add", "--all", ":/"])

if status != 0:
    sys.exit(status)

if opts.message:
    subprocess.call(["git", "commit", "-m", opts.message])
else:
    subprocess.call(["git", "commit"])
