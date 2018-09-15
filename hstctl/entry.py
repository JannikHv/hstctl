#!/usr/bin/env python3

from .utils  import validate_ip


class Entry(object):
    def __init__(self, ip, hostnames, status, comment):
        [self.ip, self.hostnames, self.status, self.comment] = [ip, hostnames, status, comment]

    @classmethod
    def new_from_line(cls, line):
        for i in line:
            if validate_ip(i.replace('#', '')):
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