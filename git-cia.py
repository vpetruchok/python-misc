#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Git add files and then commit')
parser.add_argument('-m', dest="message", help='message')
parser.add_argument('files', nargs='*', help='files to commit')
opts = parser.parse_args()

if opts.files:
    subprocess.call(["git", "add"] + opts.files)
else:
    subprocess.call(["git", "add", "--all", ":/"])

if opts.message:
    subprocess.call(["git", "commit", "-m", opts.message])
else:
    subprocess.call(["git", "commit"])
