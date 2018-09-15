#!/usr/bin/env python3

import os

from .entry import Entry


class Helper(object):
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

                entries.append(Entry(e.ip, hostnames, e.status, None))

        return entries

    @staticmethod
    def get_entries():
        if not os.access('/etc/hosts', os.R_OK):
            quit('[\033[1;31;31m-\033[0m] File not readable:\n\t/etc/hosts')

        with open('/etc/hosts', 'r') as f:
            entries = []

            for line in f.read().splitlines():
                line  = line.split()
                entry = Entry.new_from_line(line) if len(line) >= 2 else None

                if entry:
                    entries.append(entry)

        return Helper.optimize_entries(entries)