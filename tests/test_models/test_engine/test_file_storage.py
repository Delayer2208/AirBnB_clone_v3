#!/usr/bin/python3
"""
    Unit tests for the FileStorage module.
"""
import os
import time
import json
import unittest
import models
from models import storage
from models.base_model import BaseModel
from models.state import State
from models.engine.file_storage import FileStorage

db = os.getenv("HBNB_TYPE_STORAGE")


@unittest.skipIf(db == 'db', "Testing FileStorage only")
class TestFileStorage
