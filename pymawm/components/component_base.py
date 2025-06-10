import requests
import json
from pymawm.resources import response, complex_query
from pymawm.services.common_services import *
import types
import logging
from pymawm.templates.dmu import view_template



class Component(object):
    def __init__(self, activeUser, component=''):
        '''parent class for all components'''
        self.activeUser = activeUser
        if component != '':
            self._load_common_methods(component)
        self.component = component
        # self.methods = methods
        if self.methods != {}:
            self._load_methods(**self.methods)
        if 'general_services' in self.methods:
            self._load_multiple_methods(self.methods['general_services'])

    def _load_common_methods(self, component):
        for func_name, endpoint in common_search_services.items():
            endpoint = f"/{component}{endpoint}"
            self._create_search_method(func_name, endpoint)
        for func_name, endpoint in common_get_services.items():
            endpoint = f"/{component}{endpoint}"
            self._create_get_method(func_name, endpoint)
        for func_name, endpoint in common_import_services.items():
            endpoint = f"/{component}{endpoint}"
            self._create_import_method(func_name, endpoint)
        for func_name, endpoint in common_general_services.items():
            endpoint = f"/{component}{endpoint}"
            self._create_search_method('search_'+func_name, endpoint+'search')
            self._create_get_method('get_'+func_name, endpoint)
            self._create_import_method('save_'+func_name, endpoint+'save')
            self._create_delete_method('delete_'+func_name, endpoint)
            self._create_put_method('put_'+func_name, endpoint)
            self._create_bulk_import_method('bulk_import_'+func_name, endpoint+'bulkImport')
            self._create_bulk_delete_method('bulk_delete_'+func_name, endpoint+'bulkDelete')

    def _load_methods(self, search_services='', get_services='', import_services='', delete_services='', partial_update_services='', bulk_import_services='', general_services=''):
        if search_services != '':
            for func_name, endpoint in search_services.items():
                self._create_search_method(func_name, endpoint)
        if get_services != '':
            for func_name, endpoint in get_services.items():
                self._create_get_method(func_name, endpoint)
        if import_services != '':
            for func_name, endpoint in import_services.items():
                self._create_import_method(func_name, endpoint)
        if delete_services != '':
            for func_name, endpoint in delete_services.items():
                self._create_delete_method(func_name, endpoint)
        if partial_update_services != '':
            for func_name, endpoint in partial_update_services.items():
                self._create_put_method(func_name, endpoint)
        if bulk_import_services != '':
            for func_name, endpoint in bulk_import_services.items():
                self._create_bulk_import_method(func_name, endpoint)

    def _load_multiple_methods(self, general_services={}):
        if general_services == {}:
            return
        for func_name, endpoint in general_services.items():
            self._create_search_method('search_'+func_name, endpoint+'search')
            self._create_get_method('get_'+func_name, endpoint)
            self._create_import_method('save_'+func_name, endpoint+'save')
            self._create_delete_method('delete_'+func_name, endpoint)
            self._create_put_method('put_'+func_name, endpoint)
            self._create_bulk_import_method('bulk_import_'+func_name, endpoint+'bulkImport')
            self._create_bulk_delete_method('bulk_delete_'+func_name, endpoint+'bulkDelete')

    def _exec_prepared_method(self, new_func, func_name):
        exec(new_func)
        exec(f'self.{func_name}=types.MethodType({func_name},self)')

    def _create_search_method(self, func_name, endpoint):
        if endpoint.startswith('_'):
            return
        new_func = f'''def {func_name}(self, **kwargs):\n\t"""\n\tdesc\n\t"""\n\tlogging.debug('searching %s' % (kwargs))\n\tendpoint = '{endpoint}'\n\turl = self.activeUser.wm_app + endpoint\n\tquery = complex_query.parse(**kwargs)\n\tres = requests.post(url, headers=self.activeUser.headers, data=json.dumps(query))\n\treturn response._response_handler(res, verbose=self.activeUser.verbose)'''
        self._exec_prepared_method(new_func, func_name)

    def _create_get_method(self, func_name, endpoint):
        # new_func = f'''def {func_name}(self, **kwargs):\n\t"""\n\tdesc\n\t"""\n\tendpoint = '{endpoint}'\n\turl = self.activeUser.wm_app + endpoint\n\tres = requests.get(url, headers=self.activeUser.headers)\n\treturn response._response_handler(res, verbose=self.activeUser.verbose)'''
        new_func = f'''def {func_name}(self, **kwargs): \n\t"""\n\tdesc \n\t"""\n\tendpoint = '{endpoint}'\n\tparams=dict(**kwargs)\n\turl = self.activeUser.wm_app + endpoint \n\tres = requests.get(url, headers=self.activeUser.headers, params=params) \n\treturn response._response_handler(res, verbose=self.activeUser.verbose)'''
        self._exec_prepared_method(new_func, func_name)

    def _create_import_method(self, func_name, endpoint):
        new_func = f'''def {func_name}(self, data):\n\t"""\n\tjust posts whatever data is given to the function\n\t"""\n\tendpoint = '{endpoint}'\n\tif type(data) == dict:\n\t\tdata = json.dumps(data, indent=4)\n\turl = self.activeUser.wm_app + endpoint\n\tres = requests.post(url, headers=self.activeUser.headers, data=data)\n\treturn response._response_handler(res, verbose=self.activeUser.verbose)'''
        self._exec_prepared_method(new_func, func_name)

    def _create_put_method(self, func_name, endpoint):
        new_func = f'''def {func_name}(self, key, data):\n\t"""\n\tput assumes the pkey to be used comes as the last value in the url, mult-level puts (taskId/123/taskDetailId/345) not supported\n\t"""\n\tendpoint = '{endpoint}'+str(key)\n\tif type(data) == dict:\n\t\tdata = json.dumps(data)\n\turl = self.activeUser.wm_app + endpoint\n\tres = requests.put(url, headers=self.activeUser.headers, data=data)\n\treturn response._response_handler(res, verbose=self.activeUser.verbose)'''
        self._exec_prepared_method(new_func, func_name)

    def _create_delete_method(self, func_name, endpoint):
        new_func = f'''def {func_name}(self, pk):\n\t"""\n\tdesc\n\t"""\n\tendpoint = "{endpoint}"+str(pk)\n\turl = self.activeUser.wm_app + endpoint\n\tres = requests.delete(url, headers=self.activeUser.headers)\n\treturn response._response_handler(res, verbose=self.activeUser.verbose)'''
        self._exec_prepared_method(new_func, func_name)

    def _create_bulk_import_method(self, func_name, endpoint):
        new_func = f'''def {func_name}(self, data):\n\t"""\n\tdesc \n\t"""\n\tendpoint = '{endpoint}'\n\tif type(data) == dict: \n\t\tif 'data' not in [k.lower() for k in data.keys()]: \n\t\t\tdata = {{'Data':[data]}} \n\t\tdata = json.dumps(data) \n\tif type(data) == list: \n\t\tdata = {{'Data':data}} \n\t\tdata = json.dumps(data) \n\turl = self.activeUser.wm_app + endpoint \n\tres = requests.post(url, headers=self.activeUser.headers, data=data) \n\treturn response._response_handler(res, verbose=self.activeUser.verbose)'''
        self._exec_prepared_method(new_func, func_name)

    def _create_bulk_delete_method(self, func_name, endpoint):
        new_func = f'''def {func_name}(self, data):\n\t"""\n\tdesc \n\t"""\n\tendpoint = '{endpoint}'\n\tif type(data) == dict: \n\t\tif 'data' not in [k.lower() for k in data.keys()]: \n\t\t\tdata = {{'Data':[data]}} \n\t\tdata = json.dumps(data) \n\tif type(data) == list: \n\t\tdata = {{'Data':data}} \n\t\tdata = json.dumps(data) \n\turl = self.activeUser.wm_app + endpoint \n\tres = requests.post(url, headers=self.activeUser.headers, data=data) \n\treturn response._response_handler(res, verbose=self.activeUser.verbose)'''
        self._exec_prepared_method(new_func, func_name)

    def _create_log_method(self, func_name, endpoint):
        True

    def help(self):
        print(f'Methods for {self}')
        method_list = [method_name for method_name in dir(self) if callable(getattr(self, method_name)) and not method_name.startswith('__')]
        method_list.sort()
        for index, method in enumerate(method_list):
            print(f"{index+1}) {method}")

    def search_syntax(self):
        print('Not implemented yet')

    def custom_search(self, method, endpoint, query='', data=''):
        if not endpoint.startswith('/'):
            endpoint = '/' + endpoint
        url = self.activeUser.wm_app + endpoint
        if method.lower() in ['get']:
            if type(query) == dict:
                print('here here')
                query = complex_query.parse(**query)
                res = requests.request(method, url, headers=self.activeUser.headers, params=query)
                print(query)
            if data != '':
                res = requests.request(method, url, headers=self.activeUser.headers)

        if method.lower() in ['post', 'put', 'patch']:
            if type(query) == dict:
                query = complex_query.parse(**query)
                res = requests.request(method, url, headers=self.activeUser.headers, data=json.dumps(query))
            if data != '':
                res = requests.request(method, url, headers=self.activeUser.headers, data=json.dumps(data))
            else:
                res = requests.request(method, url, headers=self.activeUser.headers)
        else:
            res = requests.request(method, url, headers=self.activeUser.headers)
        return response._response_handler(res, verbose=self.activeUser.verbose)

    def run_job_by_id(self, component, job_id):
        endpoint = f'/{component}/api/batch/jobSchedule/trigger'
        url = self.activeUser.wm_app + endpoint
        data = {
            "JobScheduleId":job_id
        }
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(data))
        return response._response_handler(res, verbose=self.activeUser.verbose)    

    def get_metadata(self, component, entity):
        endpoint = f'/{component}/api/fwcore/metadata/{entity}'
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._response_handler(res, verbose=self.activeUser.verbose)

    def get_config_metadata(self, component, entity):
        endpoint = f'/{component}/api/config/metadata/{entity}'
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._response_handler(res, verbose=self.activeUser.verbose)

    def print_methods(self, service_type):
        print(self.methods[service_type])

    def run_override(self, services):
        if "general_services" in services:
            self._load_multiple_methods(services['general_services'])
        self._load_methods(**services)

    def search_view(self, view_parameters={}):
        endpoint = "/dmui-facade/api/dmui-facade/entity/search"
        if 'ComponentName' not in view_parameters:
            component_full = f"com-manh-cp-{self.component}"
            view_parameters['ComponentName'] = component_full 
        url = self.activeUser.wm_app + endpoint
        view_template.update(view_parameters)
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(view_template))
        return response._response_handler(res, verbose=False, view=True)

    def set_logs(self, log_level="DEBUG"):
        # endpoint = f'/{self.component}/component/logger/com.manh.cp.{self.component}/{log_level}' #old i guess?
        endpoint = f"/{self.component}/internal/core/admin/logs/logger/com.manh.cp/{log_level}"
        url = self.activeUser.wm_app + endpoint
        res = requests.post(url, headers=self.activeUser.headers)
        return response._response_handler(res, verbose=self.activeUser.verbose)
