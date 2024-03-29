#!/usr/bin/python3
"""File storage test module."""
from models.engine.file_storage import FileStorage
from unittest import TestCase
import unittest
import os
from models.base_model import BaseModel
from models import storage


class test_Filestorage(TestCase):
    def setUp(self):
        """Setup before each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def tearDown(self):
        """Teardown after each test."""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass
        storage._FileStorage__objects.clear()

    def test_objects_list_empty(self):
        """Initially empty __objects list."""
        self.assertEqual(len(storage.all()), 0)

    def test_empty(self):
        """Test for creating and saving in json file."""
        storage.save()
        with open('file.json', 'r') as fl:
            data = fl.read()
        self.assertNotEqual(len(data), 0)

    def test_new(self):
        """New objects added correctly to storage's __objects list."""
        new = BaseModel()
        key = f"{new.__class__.__name__}.{new.id}"
        self.assertIn(key, storage.all())

    def test_reload(self):
        """Json file loaded successfully to __objects list."""
        new = BaseModel()
        storage.save()
        storage.reload()
        key = f"{new.__class__.__name__}.{new.id}"
        self.assertIn(key, storage.all())

    def test_reload_empty(self):
        """Test reloading from an empty file"""
        with open('file.json', 'w') as fl:
            pass
        with self.assertRaises(ValueError):
            storage.reload()

    def test_reload_non_existing(self):
        """Test reloading from non-existent file."""
        self.assertEqual(storage.reload(), None)

    def test_key_format(self):
        """Test for key format."""
        new = BaseModel()
        new_id = new.to_dict()['id']
        for key in storage.all().keys():
            self.assertEqual(key, f"{new.__class__.__name__}.{new_id}")

    def test_objects_type(self):
        """Checks if __objjects is a dict."""
        self.assertEqual(type(storage.all()), dict)

    def test_created_storage_var(self):
        """Storage object created"""
        self.assertEqual(type(storage), FileStorage)

    def test_save(self):
        """Test for save method."""
        new = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_all(self):
        """Test for all method."""
        allobj = storage.all()
        self.assertIsInstance(allobj, dict)

    def test_base_model_init(self):
        """Json file not created on basemodel init."""
        new = BaseModel()
        self.assertFalse(os.path.exists('file.json'))

    def test_base_model_init2(self):
        """basemodel added to storage on init."""
        new = BaseModel()
        self.assertIn(f"{new.__class__.__name__}.{new.id}", storage.all())

    def test_base_model_save(self):
        """Storage save using basemodel save."""
        new = BaseModel()
        new.save()
        self.assertTrue(os.path.exists('file.json'))

    def test_path_type(self):
        """Ensure file path is a string."""
        self.assertEqual(type(storage._FileStorage__file_path), str)


if __name__ == "__main__":
    unittest.main()
