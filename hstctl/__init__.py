#!/usr/bin/env python3

from .argument_parser import ArgumentParser
from .entry           import Entry
from .helper          import Helper
from .hstctl          import Hstctl
from .utils           import validate_ip


def main():
    parser = ArgumentParser()

    parser.add_argument('-i', '--ips',       action='store',      dest='IPS')
    parser.add_argument('-a', '--add',       action='store',      dest='ADD_HOSTNAMES')
    parser.add_argument('-r', '--remove',    action='store',      dest='RM_HOSTNAMES')
    parser.add_argument('-e', '--enable',    action='store',      dest='ENABLE_IPS')
    parser.add_argument('-d', '--disable',   action='store',      dest='DISABLE_IPS')
    parser.add_argument('-p', '--purge',     action='store',      dest='PURGE_IPS')
    parser.add_argument('-c', '--comment',   action='store',      dest='ADD_COMMENT')
    parser.add_argument('-u', '--uncomment', action='store',      dest='RM_COMMENT')
    parser.add_argument('-s', '--show',      action='store',      dest='SHOW_IPS')
    parser.add_argument('-l', '--list',      action='store_true', dest='LIST')
    parser.add_argument('-o', '--optimize',  action='store_true', dest='OPTIMIZE')

    args = parser.parse_args()

    if args.ADD_HOSTNAMES:
        if not args.IPS:
            quit(parser.print_help())
        else:
            Hstctl.add_hostnames_by_ips(args.IPS.split(), args.ADD_HOSTNAMES.split())
            Hstctl.write()

    if args.RM_HOSTNAMES:
        if not args.IPS:
            quit(parser.print_help())
        else:
            Hstctl.remove_hostnames_by_ips(args.IPS.split(), args.RM_HOSTNAMES.split())
            Hstctl.write()

    if args.ENABLE_IPS:
        Hstctl.enable_entries_by_ips(args.ENABLE_IPS.split())
        Hstctl.write()

    if args.DISABLE_IPS:
        Hstctl.disable_entries_by_ips(args.DISABLE_IPS.split())
        Hstctl.write()

    if args.PURGE_IPS:
        Hstctl.purge_entries_by_ips(args.PURGE_IPS.split())
        Hstctl.write()

    if args.ADD_COMMENT:
        if not args.IPS:
            quit(parser.print_help())
        else:
            Hstctl.comment_entries_by_ips(args.IPS.split(), args.ADD_COMMENT)
            Hstctl.write()

    if args.RM_COMMENT:
            Hstctl.uncomment_entries_by_ips(args.RM_COMMENT.split())
            Hstctl.write()

    if args.SHOW_IPS:
        Hstctl.list_entries(args.SHOW_IPS.split())

    if args.LIST:
        Hstctl.list_entries()

    if args.OPTIMIZE:
        Hstctl.write()
