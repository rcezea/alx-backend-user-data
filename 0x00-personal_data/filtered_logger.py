#!/usr/bin/env python3
"""Filtered logging to file"""
import re
from typing import List
import logging
import os
import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ use a regex to replace occurrences of certain field values. """
    for field in fields:
        message = re.sub(f"(?<={field}=)[^{separator}]*", redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """formats logger information"""
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """return a logger instance"""
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """return an instantiated database"""
    user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db = mysql.connector.connect(user, password, host, database)
    return db


def main() -> None:
    """The function will obtain a database connection using get_db
    and retrieve all rows in the users table"""
    my_logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    for (
            name,
            email,
            phone,
            ssn,
            password,
            ip,
            last_login,
            user_agent,
    ) in cursor:
        user_details = "name={};email={};phone={};ssn={};"
        user_details += ("password={};ip={};last_login={};"
                         "user_agent={};").format(
            name, email, phone, ssn, password, ip, last_login, user_agent
        )
        my_logger.info(user_details)


if __name__ == "__main__":
    main()
