import base64
import subprocess
from pprint import pformat, pprint
# from prettyprinter import cpprint
from copy import deepcopy
import json
from re import search
from pymawm.resources.filter import key_filter, strip_ids, key_out_filter
from pymawm.resources.table import tabularize
from pymawm.resources.printer import pretty_json, pretty_py
# from pandas import json_normalize
# from types import SimpleNamespace
import logging 
logger = logging.getLogger(__name__)


# from requests.models import Response

class ActiveResponse(object):
    '''object to hold data from queries or updates
    methods do not return data, only update object data
    most methods do print results however, this is for usability and speed'''
    def __init__(self, response, verbose=True, view=False):
        self.verbose = verbose
        self.full_response = response
        self.status_code = response.status_code
        self.request = response.request
        self.subList = ''
        try:
            if view==False and response.status_code < 400:
                self.data = response.json()['data']
                self.header = response.json()['header']
            elif view==True and response.status_code < 400:
                print(response.json())
                self.data = response.json()['data']['Results']
            else:
                self.data = response.json()
            self._loadKeys()
        except json.decoder.JSONDecodeError:
            if verbose == True:
                print('Non JSON response. Check for errors.')
            self.data = response.text
            return
        except KeyError:
            self.data = response.json()
        if verbose == True:
            try:
                self.pdata()
            except KeyboardInterrupt:
                pass
        logger.info(f'Request sent to: {self.request.url}')
        logger.info(f'Response obtained {self.full_response}')

    def __repr__(self):
        return f"{type(self).__name__} Status:{self.status_code} {self.request.method}:{self.request.url}"

    def help(self):
        print(f'Methods for {self}')
        method_list = [method_name for method_name in dir(self) if callable(getattr(self, method_name)) and not method_name.startswith('__')]
        method_list.sort()
        for index, method in enumerate(method_list):
            print(f"{index+1}) {method}")

    def _loadKeys(self):
        if type(self.data) == list:
            tab_keys = set()
            for data in self.data:
                tab_keys.update(set(data.keys()))
            self.keys = list(tab_keys)
            self.keys.sort()
        elif type(self.data) == dict:
            self.keys = list(self.data.keys())
            self.keys.sort()
        return None

    def _load_sub_lists(self):
        subList = set()
        if type(self.data) == list:
            for data in self.data:
                for k, v in data.items():
                    if type(v) == list:
                        subList.update([k])
        elif type(self.data) == dict:
            for k, v in self.data.items():
                if type(v) == list:
                    subList.update(k)
                    print(f'in {data} \n adding {k}')
        return subList

    def sub_lists(self):
        if self.subList == '':
            self.subList = self._load_sub_lists()
            return self.subList
        else:
            return self.subList

    def pkeys(self):
        # cpprint(self.keys, sort_dict_keys=True)
        pretty_json(self.keys)
        return None

    # removing because pandas is too big 
    # def load_df(self, record_path=None, meta=None, meta_prefix=None, record_prefix=None, errors='raise', sep='.', max_level=None):
    #     self.df = json_normalize(self.data, record_path=record_path, meta=meta, meta_prefix=meta_prefix, record_prefix=record_prefix, errors=errors, sep=sep, max_level=max_level)
    #     return self.df


    def filterByKey(self, *keys, **subfields):
        self.fdata = key_filter(self.data, *keys, **subfields)
        self.pfilter()
        return None

    def filterOutKey(self, *keys, **subfields):
        self.fdata = key_out_filter(self.data, *keys, **subfields)
        self.pfilter()
        return None

    def pdata(self, length=None):
        # cpprint(self.data, sort_dict_keys=True)
        if length != None:
            pretty_json(self.data[:length])
        else:
            pretty_json(self.data)
        return None

    def json(self):
        # cpprint(self.full_response, sort_dict_keys=True)
        pretty_json(self.full_response.json())
        return None

    def pfilter(self):
        '''print pretty filtered data''' 
        if 'fdata' not in self.__dict__:
            print('Nothing has been filtered in this response')
        else:
            # cpprint(self.fdata, sort_dict_keys=True)
            pretty_json(self.fdata)
        return None

    def tdata(self):
        '''print table data'''
        if type(self.data) != list:
            print('Data not in form of a table')
        self.table = tabularize(self.data)
        return None

    def tfilter(self):
        '''print table of filtered data'''
        if type(self.fdata) != list:
            print('Data not in form of a table')
        self.table = tabularize(self.fdata)
        return None

    def strip_ids(self, strip_list=None, as_json=False):
        if type(strip_list) in (int, str, dict):
            print('The strip_list should be a set or list.')
            return None
        return strip_ids(self.data, strip_list=strip_list, as_json=as_json)

    def search_regex(self, query_string):
        self.search_results = []
        search_text = pformat(self.data)
        for line in search_text.split('\n'):
            if search(query_string, line):
                self.search_results.append(line)
        for line in self.search_results:    
            print(line)

    def open_json(self, editor=''):
        '''editor should be a path to text editor C:\\Program Files\\Sublime Text\\sublime_text.exe'''
        if editor == '':
            print('Please specify a default text editor')
            return
        with open('response.json', 'w') as f:
            json.dump(self.data, f, indent=4, sort_keys=True)
        subprocess.Popen([editor, 'response.json'])




#############helper functions
def _get_common_url_header(activeUser, endpoint, location=''):
    url = activeUser.wm_app + endpoint
    if location == '':
        location = activeUser.current_facility
    return [url, {
      'Content-Type': 'application/json',
      'User-Agent' : 'pymawm',
      'Authorization': activeUser.token,
      'Location' : location,
      'Organization' : activeUser.organization
    }]

def _response_handler(res, verbose=True, view=False):
    return ActiveResponse(res, verbose, view)

def _excel_response_handler(res):
    if res.status_code == 200:
        return base64.b64decode(res.json()['data'])
    else:
        print('Error Occured')
        return res

