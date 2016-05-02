#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import argparse
import urllib.request
import urllib.error
import json
import subprocess


GITHUB_REPOS_URL_TMPL = "https://api.github.com/:type/:account/repos?per_page=100&page=:page"

def mk_url(username, page_number, account_type):
    url =  GITHUB_REPOS_URL_TMPL \
        .replace(":type", account_type) \
        .replace(":account", username) \
        .replace(':page', str(page_number))
    return url

def urlopen(url):
    req = urllib.request.Request(url)
    req.add_header("Content-Type", "application/json")
    return urllib.request.urlopen(req)

def main():
    parser = argparse.ArgumentParser(description='List or clone github user''s repositories')

    parser.add_argument('-v', '--verbose',  action='store_true', help='verbose mode')
    parser.add_argument('-r', '--raw-request', dest="raw", action='store_true', help='raw request')
    parser.add_argument('-c', '--clone-all', dest="clone", action='store_true',
                        help='clone all github users'' repositories')
    parser.add_argument('-p', '--page-number', dest='page_number', type=int, default=1,
                        help='page number to process')
    parser.add_argument('username', nargs='+', help='github usernames')
    opts = parser.parse_args()
    # print(opts)

    for github_username in opts.username:
        # github_username = opts.username
        try:
            # try processing Organizations
            repos_url = mk_url(github_username, opts.page_number, 'orgs')
            response = urlopen(repos_url)
        except urllib.error.HTTPError as e:
            # try processing Individuals
            try:
                repos_url = mk_url(github_username, opts.page_number, 'users')
                response = urlopen(repos_url)
            except urllib.error.HTTPError as e:
                print(e)
                print("Headers:")
                print(e.headers)
                sys.exit(-1)

        if opts.verbose:
            print("Get data from {}".format(repos_url))

        s = response.read().decode("utf-8")
        data = json.loads(s)

        if opts.raw:
            print(data)
            sys.exit()

        for obj in data:
            clone_url = obj['clone_url']

            if opts.clone:
                subprocess.call(["git", "clone", clone_url])
            else:
                print(obj['clone_url'])

if __name__ == '__main__':
    main()
