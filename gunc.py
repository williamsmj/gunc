#!/usr/bin/env python
import argparse
import os
import subprocess


def git_status(path):
    '''Returns output of `git status --porcelain` in path'''
    process = subprocess.Popen(('git', 'status', '--porcelain'),
                               stdout=subprocess.PIPE, cwd=path)
    return process.stdout.read().splitlines()


def get_git_directories(path):
    '''Returns list of paths to git repositories below `path`'''
    check_dirs = []
    for root, dirs, files in os.walk(path):
        if '.git' in dirs:
            check_dirs.append(root)
            dirs.remove('.git')

    return check_dirs


def check_git_directories(dirs, verbose=False):
    '''
    Prints paths to git repositories containing uncommitted changes in the
    list of repositories `dir`.
    '''
    for d in dirs:
        s = git_status(d)
        if s:
            print d
            if verbose:
                print '\n'.join(s) + '\n'


def main():
    parser = argparse.ArgumentParser(
        description='Get git repositories with uncommitted changes')
    parser.add_argument('path', nargs='?', default=os.getcwd(),
                        help='path to search below ' +
                        '[working directory by default]')
    parser.add_argument('-v', dest='verbose', action='store_true',
                        help="print uncommitted files")
    args = parser.parse_args()

    dirs = get_git_directories(args.path)
    check_git_directories(dirs, verbose=args.verbose)


if __name__ == '__main__':
    main()
