#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

def search_in_path(what):
    pathlist = []
    for searchdir in os.environ.get('PATH', '').split(os.pathsep):
        path= os.path.join(searchdir, what)
        if os.path.exists(path) and not os.path.isdir(path):
            pathlist.append(path)

    for path in unique(pathlist):
        print(path)

# from http://www.peterbe.com/plog/uniqifiers-benchmark
def unique(seq):
    # order preserving
    checked = []
    for e in seq:
        if e not in checked:
            checked.append(e)
    return checked


SEARCHABLE_EXT=['', '.sh', '.bat', '.cmd', '.com', '.exe', '.py', '.rb']

if __name__ == '__main__':
    for arg in sys.argv[1:]:
        fname, fext = os.path.splitext(arg)

        if fext:
            search_in_path(fname + fext)
        else:
            for ext in SEARCHABLE_EXT:
                search_in_path(fname + ext)
