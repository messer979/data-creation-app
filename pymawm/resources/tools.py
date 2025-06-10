import json

class ActiveTools(object):
    '''class to hold various tools that can be used with active object'''
    def load_json(self, string):
        if type(string) != str:
            raise ValueError('load_json() requires a json string as input')
        self.loaded_json = json.loads(string)
        return self.loaded_json

