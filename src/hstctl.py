#!/usr/bin/env python3

import os
import argparse
import ipaddress

__author__     = 'Jannik Hauptvogel'
__email__      = 'JannikHv@gmail.com'
__maintainer__ = 'Jannik Hauptvogel'
__license__    = 'GPLv2'
__version__    = '0.1.0'


class HstArgumentParser(argparse.ArgumentParser):
    # Override
    def print_help(self):
        print('Hstctl v{} by {}.\n'.format(__version__, __author__))
        print('Usage: hstctl [OPTIONS]\n')
        print('Options:')
        print('  -h / --help                - Print help.')
        print('  -i / --ips       IPS       - IPs specifier.')
        print('  -a / --add       HOSTNAMES - Add hostnames to entries by IPs (-i).')
        print('  -r / --remove    HOSTNAMES - Remove hostnames from entries by IPs (-i).')
        print('  -e / --enable    IPS       - Enable entries by given IPs.')
        print('  -d / --disable   IPS       - Disable entries by given IPs.')
        print('  -p / --purge     IPS       - Purge entries by given IPs.')
        print('  -c / --comment   COMMENT   - Comment entries by IPs (-i).')
        print('  -u / --uncomment IPS       - Uncomment entries by given IPs.')
        print('  -s / --show      IPS       - Show entries of given IPs.')
        print('  -l / --list                - List all entries.')
        print('  -o / --optimize            - Optimize your /etc/hosts file (auto: -a/-r/-e/-d/-p/-c/-u).\n')
        print('Parameters:')
        print('  IPS       - IP Addresses (separated by spaces).')
        print('  HOSTNAMES - Hostnames (separated by spaces).')
        print('  COMMENT   - Comment/Note.')

    # Override
    def print_usage(self):
        quit(self.print_help())

    # Override
    def error(self, error):
        quit(self.print_help())


class HstHelper(object):
    @staticmethod
    def validate_ip(ip):
        try:
            ipaddress.ip_address(ip)
            return ip
        except:
            return None

    @staticmethod
    def optimize_entries(entries):
        for entry in entries:
            if [e.ip for e in entries].count(entry.ip) > 1:
                hostnames = []

                for e in [e for e in entries if e.ip == entry.ip]:
                    for h in e.hostnames:
                        if h not in hostnames:
                            hostnames.append(h)

                    entries.remove(e)

                entries.append(HstEntry(e.ip, hostnames, e.status, None))

        return entries

    @staticmethod
    def get_entries():
        if not os.access('/etc/hosts', os.R_OK):
            quit('[\033[1;31;31m-\033[0m] File not readable:\n\t/etc/hosts')

        with open('/etc/hosts', 'r') as f:
            entries = []

            for line in f.read().splitlines():
                line  = line.split()
                entry = HstEntry.new_from_line(line) if len(line) >= 2 else None

                if entry:
                    entries.append(entry)

        return HstHelper.optimize_entries(entries)


class HstEntry(object):
    def __init__(self, ip, hostnames, status, comment):
        [self.ip, self.hostnames, self.status, self.comment] = [ip, hostnames, status, comment]

    @classmethod
    def new_from_line(cls, line):
        for i in line:
            if HstHelper.validate_ip(i.replace('#', '')):
                ip        = i.replace('#', '')
                hostnames = [
                    h for h in line[line.index(i) + 1::]
                    if '#' not in ''.join(line[line.index(i) + 1:line.index(h) + 1:])
                    and '#' not in h
                ]
                status    = False if '#' in ''.join(line[:line.index(i) + 1:]) else True
                comment   = ' '.join(line[line.index(hostnames[-1]) + 1::]) if hostnames else None

                if comment:
                    comment = comment[2::] if comment[1] == ' ' else comment[1::]

                return cls(ip, hostnames, status, comment) if len(hostnames) > 0 else None

        return None


class Hstctl(object):
    __entries = HstHelper.get_entries()

    @staticmethod
    def add_hostnames_by_ips(ips, hostnames):
        for e in [e for e in Hstctl.__entries if e.ip in ips]:
            e.hostnames += [h for h in hostnames if h not in e.hostnames]

        for ip in [i for i in ips if i not in [e.ip for e in Hstctl.__entries]]:
            if HstHelper.validate_ip(ip) and len(hostnames) > 0:
                Hstctl.__entries.append(HstEntry(ip, hostnames, True, None))

    @staticmethod
    def remove_hostnames_by_ips(ips, hostnames):
        for e in [e for e in Hstctl.__entries if e.ip in ips]:
            e.hostnames = list(set(e.hostnames) - set(hostnames))

            if len(e.hostnames) is 0:
                Hstctl.__entries.remove(e)

    @staticmethod
    def enable_entries_by_ips(ips):
        for e in [e for e in Hstctl.__entries if e.ip in ips]:
            e.status = True

    @staticmethod
    def disable_entries_by_ips(ips):
        for e in [e for e in Hstctl.__entries if e.ip in ips]:
            e.status = False

    @staticmethod
    def purge_entries_by_ips(ips):
        for e in [e for e in Hstctl.__entries if e.ip in ips]:
            Hstctl.__entries.remove(e)

    @staticmethod
    def comment_entries_by_ips(ips, comment):
        for e in [e for e in Hstctl.__entries if e.ip in ips]:
            e.comment = comment

    @staticmethod
    def uncomment_entries_by_ips(ips):
        for e in [e for e in Hstctl.__entries if e.ip in ips]:
            e.comment = None

    @staticmethod
    def list_entries(ips = []):
        max_len = 4

        for e in Hstctl.__entries:
            if (not ips or e.ip in ips) and max_len < len(e.ip):
                max_len = len(e.ip)

        print('\033[1;34;34mStatus   ' + 'IP'.ljust(max_len, ' ') + ' Hostnames\033[0m')

        for e in Hstctl.__entries:
            if not ips or e.ip in ips:
                if e.status:
                    print('\033[1;32;32mEnabled\033[0m  ' + e.ip.ljust(max_len, ' '), e.hostnames)
                else:
                    print('\033[1;31;31mDisabled\033[0m ' + e.ip.ljust(max_len, ' '), e.hostnames)

                if e.comment:
                    print( '\033[1;34;34m  ->\033[0m \033[1;33;33m' + e.comment + '\033[0m \n')

    @staticmethod
    def write():
        if not os.access('/etc/hosts', os.W_OK):
            quit('[\033[1;31;31m-\033[0m] File not writable:\n\t/etc/hosts')

        with open('/etc/hosts', 'w+') as f:
            f.write('##\n# This file was generated by Hstctl.\n##\n\n')

            for e in Hstctl.__entries:
                status_prefix  = '' if e.status else '# '
                comment_prefix = ' # ' + e.comment if e.comment else ''

                f.write(status_prefix + e.ip + ' ' + ' '.join(e.hostnames) + comment_prefix + '\n')

        f.close()


if __name__ == '__main__':
    parser = HstArgumentParser()

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
