#!/usr/bin/env python3
"""Filtered logging to file"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ use a regex to replace occurrences of certain field values. """
    for field in fields:
        message = re.sub(f"(?<={field}=)[^{separator}]*", redaction, message)
    return message
