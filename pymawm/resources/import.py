from copy import deepcopy

def purge_json(data):
    purge_list = {'Messages', 'PK', 'Unique_Identifier', 'ContextId'}
    d_copy = deepcopy(data)
    for key, value in d_copy.items():
        if key in purge_list:
            del data[key]
        if type(value) == dict:
            data[key] = purge_json(value)
    return data