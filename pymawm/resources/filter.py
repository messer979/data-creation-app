from copy import deepcopy
import logging
import json
from pymawm.resources.printer import pretty_json, pretty_py

#support library for filtering nested json data
#key_filter is called when using the filter method in the response class
#uses a simple syntax for filtering - sample for filtering a user search response (see org tools): 
# key_filter(res.data, 'UserId', **{'OrgUser':['User', {'UserRole': ['RoleId', {'OrgUser': ['OrganizationId']}]}]})


def key_filter(obj, *keys, **subfields):
    '''*keys should be a list of keys to be returned in the filtered object.'''
    if type(obj) == list:
        filtered_data_list = []
        for filtered_data in deepcopy(obj):
            filtered_data = {k:v for k,v in filtered_data.items() if k in keys or k in subfields.keys()}
            for key, value in filtered_data.items():
                if key not in subfields.keys():
                    continue
                elif type(value) == list:
                    new_args, new_kwargs = _parse_arg(*subfields[key])
                    filtered_data[key] = _filter_list_subfield(filtered_data[key], *new_args, **new_kwargs)
                elif type(value) == dict:
                    new_args, new_kwargs = _parse_arg(*subfields[key])
                    filtered_data[key] = _filter_dict_subfield(filtered_data[key], *new_args, **new_kwargs)
            filtered_data_list.append(filtered_data)
        return filtered_data_list
    elif type(obj) == dict:
        filtered_data = deepcopy(obj)
        filtered_data = {k:v for k,v in filtered_data.items() if k in keys or k in subfields.keys()}
        for key, value in filtered_data.items():
            if key not in subfields.keys():
                continue
            elif type(value) == list:
                new_args, new_kwargs = _parse_arg(*subfields[key])
                filtered_data[key] = _filter_list_subfield(filtered_data[key], *new_args, **new_kwargs)
            elif type(value) == dict:
                new_args, new_kwargs = _parse_arg(*subfields[key])
                filtered_data[key] = _filter_dict_subfield(filtered_data[key], *new_args, **new_kwargs)
        return filtered_data

def key_out_filter(obj, *keys, **subfields):
    '''*keys should be a list of keys to be returned in the filtered object.'''
    if type(obj) == list:
        filtered_data_list = []
        for filtered_data in deepcopy(obj):
            filtered_data = {k:v for k,v in filtered_data.items() if k not in keys or k in subfields.keys()}
            for key, value in filtered_data.items():
                if key not in subfields.keys():
                    continue
                elif type(value) == list:
                    new_args, new_kwargs = _parse_arg(*subfields[key])
                    filtered_data[key] = _filter_list_subfield(filtered_data[key], *new_args, **new_kwargs)
                elif type(value) == dict:
                    new_args, new_kwargs = _parse_arg(*subfields[key])
                    filtered_data[key] = _filter_dict_subfield(filtered_data[key], *new_args, **new_kwargs)
            filtered_data_list.append(filtered_data)
        return filtered_data_list
    elif type(obj) == dict:
        filtered_data = deepcopy(obj)
        filtered_data = {k:v for k,v in filtered_data.items() if k not in keys or k in subfields.keys()}
        for key, value in filtered_data.items():
            if key not in subfields.keys():
                continue
            elif type(value) == list:
                new_args, new_kwargs = _parse_arg(*subfields[key])
                filtered_data[key] = _filter_list_subfield(filtered_data[key], *new_args, **new_kwargs)
            elif type(value) == dict:
                new_args, new_kwargs = _parse_arg(*subfields[key])
                filtered_data[key] = _filter_dict_subfield(filtered_data[key], *new_args, **new_kwargs)
        return filtered_data


def _filter_dict_subfield(subfield, *keys, **subfields):
    new_item = {k:v for k,v in subfield.items() if k not in keys or k in subfield.keys()}
    for key, value in new_item.items():
        if key not in subfields:
            continue
        elif type(value) == dict:
            new_args, new_kwargs = _parse_arg(*subfields[key])
            new_item[key] = _filter_dict_subfield(value, *new_args, **new_kwargs)
        elif type(value) == list:
            new_args, new_kwargs = _parse_arg(*subfields[key])
            new_item[key] = _filter_list_subfield(value, *new_args, **new_kwargs)
    return subfield

def _filter_list_subfield(subfield, *keys, **subfields):
    new_subfield = []
    for subfield_item in subfield:
        new_item = {k:v for k,v in subfield_item.items() if k not in keys or k in subfields.keys()}
        for key, value in new_item.items():
            if key not in subfields:
                continue
            elif type(value) == dict:
                new_args, new_kwargs = _parse_arg(*subfields[key])
                new_item[key] = _filter_dict_subfield(value, *new_args, **new_kwargs)
            elif type(value) == list:
                new_args, new_kwargs = _parse_arg(*subfields[key])
                new_item[key] = _filter_list_subfield(value, *new_args, **new_kwargs)
        new_subfield.append(new_item)
    return new_subfield

def _parse_arg(*arg_list):
    new_args = []
    new_kwargs = {}
    for arg in arg_list:
        if type(arg) != dict:
            new_args.append(arg)
        else:
            new_kwargs=arg
            return new_args, new_kwargs
    logging.debug(f"from _parse_args: {(new_args, {'_ ': ' '})}")
    return new_args, {'_ ': ' '}



def strip_ids(obj, strip_list=None, as_json=False):
    def _strip_sub_obj_ids(obj, strip_list):
        if type(obj) == list:
            for item in obj:
                _strip_sub_obj_ids(item, strip_list)
        elif type(obj) == dict:
            for s in strip_list:
                if s in obj:
                    del obj[s]
            for key, value in obj.items():
                if type(value) in (list, dict):
                    _strip_sub_obj_ids(value, strip_list)
    output_obj = deepcopy(obj)
    if strip_list == None:
        strip_list = {'ContextId', 'PK', 'CreatedBy', 'UpdatedBy', 'CreatedTimestamp', 'UpdatedTimestamp', 'Unique_Identifier'}
    elif type(strip_list) == list:
        strip_list = set(strip_list)
    _strip_sub_obj_ids(output_obj, strip_list)
    if as_json == True:
        return json.dumps(output_obj)
    else:
        return output_obj

