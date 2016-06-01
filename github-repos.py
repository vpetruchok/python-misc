#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import argparse
import urllib.request
import urllib.error
import json
import subprocess

GITHUB_REPOS_URL_TMPL = "https://api.github.com/:account_type/:account/repos?per_page=100&page=:page_number"

def mk_url(account_type, account, page_number):
    url = GITHUB_REPOS_URL_TMPL \
        .replace(":account_type", account_type) \
        .replace(":account", account) \
        .replace(':page_number', str(page_number))
    return url

def urlopen(url):
    req = urllib.request.Request(url)
    req.add_header("Content-Type", "application/json")
    return urllib.request.urlopen(req)

def get_username(username_or_url):
    parts = username_or_url.split('/')
    if len(parts) == 1:
        return parts[0]
    else:
        return parts[3]

def main():
    parser = argparse.ArgumentParser(description='List or clone github user''s repositories')

    parser.add_argument('-v', '--verbose',  action='store_true', help='verbose mode')
    parser.add_argument('-r', '--raw-response', dest="raw", action='store_true',
            help='show unparsed raw response')
    parser.add_argument('-c', '--clone-all', dest="clone", action='store_true',
                        help='clone all user\'s repositories')
    parser.add_argument('-p', '--page-number', dest='page_number', type=int, default=1,
                        help='page number to process')
    parser.add_argument('username_or_url', nargs='+', help='github usernames or repository urls')
    opts = parser.parse_args()
    # print(opts)

    for username_or_url in opts.username_or_url:
        github_username = get_username(username_or_url)
        try:
            # try processing Organizations
            repos_url = mk_url('orgs', github_username, opts.page_number)
            response = urlopen(repos_url)
        except urllib.error.HTTPError as e:
            # try processing Individuals
            try:
                repos_url = mk_url('users', github_username, opts.page_number)
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
                print(clone_url)

if __name__ == '__main__':
    main()
