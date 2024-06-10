#!/usr/bin/python3
"""
Defines the FileStorage class for file storage
"""
import json
import models


class FileStorage:
    """
    Serializes instances to a JSON file and deserializes JSON file to instances
    """
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Return the dictionary of all objects
        """
        if cls:
            filtered_dict = {}
            for key, value in self.__objects.items():
                if key.startswith(cls.__name__ + "."):
                    filtered_dict[key] = value
            return filtered_dict
        return self.__objects

    def new(self, obj):
        """
        Add a new object to the storage
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        Serialize the objects to a JSON file
        """
        with open(self.__file_path, 'w', encoding='utf-8') as f:
            temp_dict = {key: val.to_dict() for key, val in self.__objects.items()}
            json.dump(temp_dict, f)

    def reload(self):
        """
        Deserialize the JSON file to objects
        """
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as f:
                temp_dict = json.load(f)
                for key, val in temp_dict.items():
                    class_name = val["__class__"]
                    self.__objects[key] = models.classes[class_name](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Delete an object from the storage
        """
        if obj:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
                self.save()

    def close(self):
        """
        Call reload method for deserializing the JSON file to objects
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieve an object based on the class and its ID
        """
        if cls and id:
            key = f"{cls.__name__}.{id}"
            return self.__objects.get(key)
        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage
        """
        return len(self.all(cls))
