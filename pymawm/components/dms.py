import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.dmu import *
from pymawm.templates.dmu import *

#transactions
class DMUISearch(Component):
    def __init__(self, activeUser):
        '''dmui-search/api/dmui-search'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, general_services=general_services, get_services=get_services)
        super().__init__(activeUser, 'dmui-search')

    def search_activity_tracking(self, view_parameters={}):
        endpoint = "/dmui-search/api/dmui-facade/entity/search"
        url = self.activeUser.wm_app + endpoint
        activity_view_template.update(view_parameters)
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(activity_view_template))
        return response._response_handler(res, verbose=False, view=True)

    def search_ym_visit(self, view_parameters={}):
        endpoint = "/dmui-search/api/dmui-facade/entity/search"
        url = self.activeUser.wm_app + endpoint
        ym_visit_view_template.update(view_parameters)
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(ym_visit_view_template))
        return response._response_handler(res, verbose=False, view=True)

    def search_item_inventory(self, item_view={}):
        endpoint = "/dmui-search/api/dmui-facade/inventory/itemInventory/search"
        url = self.activeUser.wm_app + endpoint
        item_inventory_view_template.update(item_view)
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(item_inventory_view_template))
        return response._response_handler(res, verbose=False, view=True)

    def search_component(self, component_name):
        endpoint = "/dmui-search/api/dmui-facade/config/attribute/{component_name}"
        url = self.activeUser.wm_app + endpoint
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(activity_view_template))
        return response._response_handler(res, verbose=False, view=True)        

    def search_lookup_keys(self, component_name, view_name):
        endpoint = f"/dmui-search/api/dmui-facade/extension/view/lookupKeys/{component_name}/{view_name}"
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._response_handler(res, verbose=False)

    # def search_view(self, component_name, view_name, view_parameters):
    #     endpoint = "/dmui-search/api/dmui-facade/entity/search"
    #     url = self.activeUser.wm_app + endpoint
    #     view_template.update(view_parameters)
    #     res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(view_template))
    #     return response._response_handler(res, verbose=False)

    # def search_(self, component_name, view_name):
    #     endpoint = f"/dmui-search/api/dmui-facade/extension/view/lookupKeys/{component_name}/{view_name}"
    #     url = self.activeUser.wm_app + endpoint
    #     res = requests.get(url, headers=self.activeUser.headers)
    #     return response._response_handler(res, verbose=False)        
