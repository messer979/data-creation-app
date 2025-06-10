import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.itm import *

class Item(Component):
    def __init__(self, activeUser):
        '''/item-master/api/item-master'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services)
        super().__init__(activeUser, 'item-master')

    #search methods
    def quick_get(self, service, **kwargs):
        endpoint = f"/item-master/api/item-master/{service}"
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._response_handler(res)

    def quick_search_item(self, item):
        endpoint = '/item-master/api/item-master/item/search'
        query = {
            "Query": f"ItemId~{item}"
            }
        url = self.activeUser.wm_app + endpoint
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(query))
        return response._response_handler(res)

    #excel methods
    def get_excel_template(self):
        '''this returns the template only, better to use the actual export'''
        endpoint = '/item-master/api/item-master/item/excelTemplate'
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._excel_response_handler(res)

    def get_excel_export(self):
        endpoint = '/item-master/api/item-master/item/exportExcel'
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._excel_response_handler(res)

    def post_excel_export(self, excelfile):
        endpoint = '/item-master/api/item-master/item/importExcel'
        url = self.activeUser.wm_app + endpoint
        files=[
            ('workbook',('Item.xlsx',open(excelfile,'rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        ]
        del headers['Content-Type']
        res = requests.post(url, headers=self.activeUser.headers, data={}, files=files)
        return response._excel_response_handler(res)