#!/usr/bin/env python3
"""Filtered logging to file"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str):
    """ use a regex to replace occurrences of certain field values. """
    b = message.split(separator)[0:-1]
    for field in fields:
        b = [re.sub(rf'^{field}=[A-Za-z0-9_/]+', f"{field}={redaction}", item)
             if item.startswith(field) else item for item in b]
    return separator.join(b)
