import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.dci import *
from pymawm.templates.dci import *

class DCInv(Component):
    def __init__(self, activeUser):
        '''dcinventory/api/dcinventory'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services, import_services=import_services)
        super().__init__(activeUser, 'dcinventory')


    def load_allocatable_inv(self, itemId):
        endpoint = '/dcinventory/api/dcinventory/loadInventory/allocatableInventory'
        url = self.activeUser.wm_app + endpoint
        payload = {
            "ItemId": itemId
            }
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(payload))
        return response._response_handler(res)    

    def import_ilpn_and_inv(self, data):
        endpoint = '/dcinventory/api/dcinventory/ilpn/createIlpnAndInventory'
        url = self.activeUser.wm_app + endpoint
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(data))
        return response._response_handler(res, verbose=self.activeUser.verbose)


    ##quick methods
    def quick_search_inventory(self, inventory_id):
        endpoint = '/dcinventory/api/dcinventory/inventory/search'
        url = self.activeUser.wm_app + endpoint
        query = {
            "Query": f"InventoryId~{inventory_id}"
            }
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(query))
        return response._response_handler(res)

    def quick_search_inventory_ItemId(self, item):
        endpoint = '/dcinventory/api/dcinventory/inventory/search'
        url = self.activeUser.wm_app + endpoint
        query = {
            "Query": f"ItemId~{item}"
            }
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(query))
        return response._response_handler(res)

    def quick_search_ilpn(self, IlpnId):
        endpoint = '/dcinventory/api/dcinventory/ilpn/ilpninventorysearch'
        url = self.activeUser.wm_app + endpoint
        query = {
            "Query": f"IlpnId~{IlpnId}"
            }
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(query))
        return response._response_handler(res)

    def quick_search_locations(self, LocationId):
        endpoint = '/dcinventory/api/dcinventory/location'
        url = self.activeUser.wm_app + endpoint
        query = {
            "Query": f"LocationId~{LocationId}"
            }
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(query))
        return response._response_handler(res)
