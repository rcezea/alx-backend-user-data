#!/usr/bin/env python3
"""Filtered logging to file"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """ use a regex to replace occurrences of certain field values. """
    b = message.split(separator)
    for i, item in enumerate(message.split(separator)):
        for field in fields:
            if item.startswith(field):
                b[i] = re.sub(rf'^{field}=[A-Za-z0-9_/]+',
                              f"{field}={redaction}", item)
    return separator.join(b)
