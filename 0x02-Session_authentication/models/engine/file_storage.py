#!/usr/bin/env python3
"""
FileStorage module
"""

class FileStorage:
    """
    FileStorage class
    """
    __objects = {}

    def all(self, cls=None):
        """
        Return the dictionary of all objects
        """
        if cls is not None:
            return {k: v for k, v in self.__objects.items() if isinstance(v, cls)}
        return self.__objects

    def new(self, obj):
        """
        Add a new object to the storage
        """
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """
        Save the objects to the file (not implemented for in-memory storage)
        """
        pass

    def delete(self, obj=None):
        """
        Delete an object from the storage
        """
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            if key in self.__objects:
                del self.__objects[key]
