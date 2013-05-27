import os, sys, json

class JsonSettings:
    def __init__(self, path=None, data=None):
        self._data = None
        self.path = path

        if data: self.data = data 


    def load(self, path=None):

        self.path = path if path else self.path

        if not path:
            raise ValueError("No path specified to load")
        try:
            file = open(path, encoding='utf-8', mode='r')
        except OSError as e:
            raise e
        else:
            try:
                self._data = json.load(file)
            except ValueError as e:
                raise e

                        
    def save(self, path=None, data=None):
        path = path if path else self.path
        data = data if data else self.data

        if not path or not data:
            raise ValueError("JsonSettings path or data not set") 
        try:
            with open(path, encoding='utf-8', mode='w+') as file:
                    file.write(json.dumps(data, indent=4, separators=(',', ': ')))
                    file.close()
        except OSError as e:
            print("File error "+e.errno)            
        
    @property
    def data(self):
        return self._data
    @data.setter
    def data(self, data):
        try:
            if isinstance(data, dict):
                self._data = data
            elif isinstance(data, basestring):    
                data = json.loads(data)
            else:
                raise ValueError("Data must be string or dictionary")    
            self._data = data            
        except ValueError as e:
            print("Not valid json")    
