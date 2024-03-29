#!/usr/bin/python3
"""FileStorage class module."""
import json
from models.user import User
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """This is a storage class that stor all data."""
    __file_path = "file.json"
    __objects = {}

    class_mapping = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Place': Place,
        'Amenity': Amenity,
        'Review': Review
    }

    def all(self):
        """All func for storage."""
        return FileStorage.__objects

    def save(self):
        """Save func for storage."""
        objects = {}
        for name, obj in FileStorage.__objects.items():
            objects[name] = obj.to_dict()
        with open(FileStorage.__file_path, 'w') as fl:
            json.dump(objects, fl)

    def new(self, obj):
        """New func for storage."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        FileStorage.__objects[key] = obj

    def reload(self):
        """Reload func for storage."""
        try:
            with open(FileStorage.__file_path) as fl:
                objects = json.load(fl)
                for key, object_info in objects.items():
                    cls_name, id = key.split('.')
                    if cls_name in self.class_mapping:
                        cls = self.class_mapping[cls_name]
                        instance = cls(**object_info)
                    FileStorage.__objects[key] = instance
        except FileNotFoundError:
            return
