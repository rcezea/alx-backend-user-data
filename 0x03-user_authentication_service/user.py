#!/usr/bin/env pyhton3
""" 0x03. User authentication service """


from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """
    create a SQLAlchemy model named User for a database table named users
    """
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        """ user representation"""
        return ("<User(id='%s', email='%s', hashed_password='%s',"
                "session_id='%s', reset_token='%s')>") % (
                                         self.id, self.email,
                                         self.hashed_password,
                                         self.session_id, self.reset_token)
