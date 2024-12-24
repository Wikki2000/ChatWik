#!/usr/bin/python3
"""This module models the storage of the authentication API"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from dotenv import load_dotenv
from os import getenv
from typing import Type, Any, List
from sqlalchemy import or_

load_dotenv()

class Storage:
    """ Defines storage model using SQLAlchemy. """
    __session = None
    __engine = None

    def __init__(self):
        """ Create session engine to interact with database. """
        username = getenv('CHATWIK_USER_NAME')
        password = getenv('CHATWIK_PASSWORD')
        database = getenv('CHATWIK_DATABASE')

        if not username or not password:
            error = "Environment variables must be set for database URL"
            raise ValueError(error)

        url = f'mysql+mysqldb://{username}:{password}@localhost:5432/{database}'
        self.__engine = create_engine(url, pool_pre_ping=True)
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine)
        self.__session = scoped_session(session_factory)

    def all(self, cls=None):
        """Retrieve data from database."""
        new_dict = {}

        rows = self.__session.query(cls).all()
        for row in rows:
            key = f"{row.__class__.__name__}.{row.id}"
            new_dict.update({key: row})
        return new_dict

    def get_session(self):
        """ Get the session engine for connecting to the database. """
        return self.__session

    def get_engine(self):
        """ Get the engine object """
        return self.__engine

    def new(self, obj):
        """ Add user object to session.new """
        self.__session.add(obj)

    def rollback(self):
        """ Rollback a session on error. """
        self.__session.rollback()

    def get_by_id(self, cls, obj_id):
        """Retrieve an instance with it's ID."""
        obj = self.__session.query(cls).filter_by(id=obj_id).first()
        return obj

    def get_by_field(self, model: Type, field: str, value: Any) -> object:
        """
        General function to filter a model by it field and class.

        :param model - SQLAlchemy model class (e.g., Lecturer, Student etc.)
        :param field - The colum or attribute to filter for in the model
        :param value - The corresponding value of field to filter on

        :rtype - The first matching object or None if not found
        """
        try:

            # Get the attributes and filter by it corresponding value.
            return self.__session.query(model).filter(
                getattr(model, field) == value
            ).all()
        except AttributeError:
            return None

    def get_by_double_field(
        self, model: Type, attr_val1: List, attr_val2: List
    ) -> List:
        """
        Filter a modell using two field.

        :attr_val1 - List of attribute and value of 1st field.
        :attr_val2 - List of attribute and value of 2nd field.

        :rtype - List of the search result.
        """
        sender_id = getattr(model, attr_val1[0])
        receiver_id = getattr(model, attr_val2[0])
        result = (
            self.__session.query(model)
            .filter(
                or_(
                    (sender_id == attr_val1[1]) & (receiver_id == attr_val2[1]),
                    (receiver_id == attr_val1[1]) & (sender_id == attr_val2[1])
                )
            )
            .all()
        )
        return result

    def save(self):
        """ Commit change to database """
        self.__session.commit()

    def delete(self, obj):
        """ Delete an instance of a class. """
        self.__session.delete(obj)

    def close(self):
        """ Close database session. """
        self.__session.close()
