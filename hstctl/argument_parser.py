#!/usr/bin/env python3

import argparse

from .info import (
    __version__,
    __author__
)


class ArgumentParser(argparse.ArgumentParser):
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