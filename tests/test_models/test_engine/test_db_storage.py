#!/usr/bin/python3
"""
    Unit tests for the DBStorage module.
"""
import time
import unittest
import sys
from models.engine.db_storage import DBStorage
from models import storage
from models.user import User
from models.state import State
from console import HBNBCommand
from os import getenv
from io import StringIO

db = getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(db != 'db', "Testing DBStorage only")
class TestDBStorage(unittest.TestCase):
    """
        Tests for the DBStorage class
    """
    @classmethod
    def setUpClass(cls):
        """
            Set up for the test cases
        """
        cls.dbstorage = DBStorage()
        cls.output = StringIO()
        sys.stdout = cls.output

    @classmethod
    def tearDownClass(cls):
        """
            Clean up after the test cases
        """
        del cls.dbstorage
        del cls.output

    def create_console(self):
        """
            Create an instance of HBNBCommand
        """
        return HBNBCommand()

    def test_new_state(self):
        """
            Test creating a new State instance
        """
        new_obj = State(name="California")
        self.assertEqual(new_obj.name, "California")

    def test_dbstorage_user_attributes(self):
        """
            Test User attributes
        """
        new = User(email="melissa@hbtn.com", password="hello")
        self.assertEqual(new.email, "melissa@hbtn.com")

    def test_dbstorage_methods(self):
        """
            Check if DBStorage methods exist
        """
        self.assertTrue(hasattr(self.dbstorage, "all"))
        self.assertTrue(hasattr(self.dbstorage, "__init__"))
        self.assertTrue(hasattr(self.dbstorage, "new"))
        self.assertTrue(hasattr(self.dbstorage, "save"))
        self.assertTrue(hasattr(self.dbstorage, "delete"))
        self.assertTrue(hasattr(self.dbstorage, "reload"))

    def test_all_method(self):
        """
            Test the all method
        """
        storage.reload()
        result = storage.all("")
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 0)
        new_user = User(email="adriel@hbtn.com", password="abc")
        console = self.create_console()
        console.onecmd("create State name=California")
        result = storage.all("State")
        self.assertTrue(len(result) > 0)

    def test_new_save_method(self):
      
