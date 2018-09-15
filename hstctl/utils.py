#!/usr/bin/env python3

import ipaddress


def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return ip
    except:
        return None
