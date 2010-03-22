##
# Copyright (c) 2010 Sprymix Inc.
# All rights reserved.
#
# See LICENSE for details.
##


import os
import sys

import py
from semantix.utils import shell


class TestCommand(shell.Command, expose=True):
    name = 'test'

    def get_parser(self, subparsers):
        parser = super().get_parser(subparsers)

        parser.add_argument('--keep-going', action='store_true', default=False)
        parser.add_argument('--color', action='store_true', default=True)
        parser.add_argument('--no-color', dest='color', action='store_false')
        parser.add_argument('-d', '--debug', dest='debug', action='append')
        parser.add_argument('tests', nargs='*')

        return parser

    def __call__(self, args):
        test_args = []

        test_args.extend(('-p', 'semantix', '-s'))

        if args.debug:
            test_args.extend('--semantix-debug=%s' % d for d in args.debug)
            test_args.append('--capture=no')

        if args.tests:
            test_args.extend('--tests=%s' % t for t in args.tests)
            test_args.extend(('-k', 'testmask'))

        if args.color:
            test_args.append('--colorize')

        if not args.keep_going:
            test_args.append('-x')

        path = os.path.dirname(os.path.abspath(__file__))

        # This ugliness is required due to py.test braindead plugin lookup: there is
        # no way to specify a plugin with full package path, only a name _suffix_
        sys.path.insert(0, path)
        py.test.cmdline.main(test_args)
        sys.path.remove(path)
