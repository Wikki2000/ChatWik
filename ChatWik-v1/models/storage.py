#!/usr/bin/python3
"""This module models the storage of the authentication API"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base_model import Base
from dotenv import load_dotenv
from os import getenv

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
        session = sessionmaker(bind=self.__engine)
        self.__session = session()

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

    def save(self):
        """ Commit change to database """
        self.__session.commit()

    def delete(self, obj):
        """ Delete an instance of a class. """
        self.__session.delete(obj)

    def close(self):
        """ Close database session. """
        self.__session.close()
