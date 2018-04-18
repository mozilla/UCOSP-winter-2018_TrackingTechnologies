
import os
import json


"""
A simple cache for storing data in a json file
Current use case: is for reducing the amount of requests to Cookiepedia
"""
class Simple_Json_Cache:
    file_name = None
    file_data = {}

    def __init__(self, cache_name):
        """ creates cache storage location and loads data from disk if available """
        self.file_name = '.cache/{}.json'.format(cache_name)

        if not os.path.exists(os.path.dirname(self.file_name)):
            os.makedirs(os.path.dirname(self.file_name)) 
            
        if os.path.isfile(self.file_name):
            self.file_data = self.get_cache_file()
            
            
    def get_value(self, key):
        """ gets value from in memory cache """
        return self.file_data.get(key, None)

    def set_value(self, key, value):
        """ adds value to in memory cache """
        self.file_data[key] = value

    def dump(self):
        """ pushes memory cache into file """
        with open(self.file_name, 'w+') as out_file:
            json.dump(self.file_data, out_file)

    def get_cache_file(self):
        """ returns the cache file. Mainly for the class and debugging purpose """
        data = {}
        with open(self.file_name) as json_data:
            data = json.load(json_data)
        return data

    def get_cache_memory(self):
        """ returns the current memory as a dict for looping over """
        return self.file_data