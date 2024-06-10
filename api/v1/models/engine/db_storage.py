#!/usr/bin/python3
"""
Defines the DBStorage class for database storage
"""
from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
import models
from models.state import State
from models.city import City
from models.base_model import Base


class DBStorage:
    """
    SQLAlchemy storage for the database
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initialize the database storage engine
        """
        user = getenv("HBNB_MYSQL_USER")
        password = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        database = getenv("HBNB_MYSQL_DB")
        environment = getenv("HBNB_ENV", "none")
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{database}', pool_pre_ping=True
        )
        if environment == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query the current database session for objects
        """
        objects_dict = {}

        if cls:
            if isinstance(cls, str):
                cls = models.classes[cls]
            instances = self.__session.query(cls).all()
            for instance in instances:
                key = f"{instance.__class__.__name__}.{instance.id}"
                objects_dict[key] = instance
            return objects_dict
        else:
            for class_name, class_type in models.classes.items():
                if class_name != "BaseModel":
                    instances = self.__session.query(class_type).all()
                    for instance in instances:
                        key = f"{instance.__class__.__name__}.{instance.id}"
                        objects_dict[key] = instance
            return objects_dict

    def new(self, obj):
        """
        Add an object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit the changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete an object from the current database session
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reload the database by creating all tables
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Close the current session
        """
        self.__session.remove()

    def get(self, cls, id):
        """
        Retrieve one object based on the class and its ID
        """
        if cls and id:
            cls_dict = self.all(cls)
            return cls_dict.get(f"{cls}.{id}")
        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage
        """
        return len(self.all(cls))
