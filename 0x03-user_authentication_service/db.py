#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Create a new user"""
        user = User(email=email, hashed_password=hashed_password)
        session = self._session
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """ return a specific user """
        if kwargs:
            session = self._session
            for key in kwargs.keys():
                try:
                    user_obj = (
                        session.query(User)
                        .filter(getattr(User, key) == kwargs.get(key))
                        .first()
                    )
                    if user_obj:
                        return user_obj
                except AttributeError:
                    raise InvalidRequestError
            raise NoResultFound
        raise NoResultFound

    def update_user(self, user_id: int, **kwargs) -> None:
        """ Update a specific user """
        user = self.find_user_by(id=user_id)
        session = self._session
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError
        session.commit()
