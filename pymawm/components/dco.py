import requests
import json
import base64
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.dco import *

class Dco(Component):
    def __init__(self, activeUser):
        '''/dcorder/api/dcorder'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services)
        super().__init__(activeUser, 'dcorder')

    ##search methods
    def quick_search_order(self, order):
        endpoint = "/dcorder/api/dcorder/order/search"
        url = self.activeUser.wm_app + endpoint
        query = {
            "Query": f"OrderId~{order}",
            "MaximumStatus":9000,
            "MinimumStatus":9000
            }
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(query))
        return response._response_handler(res)

    ##update methods
    def cancel_order(self, order_id):
        endpoint = f"/dcorder/api/dcorder/order/orderId/{order_id}"
        url = self.activeUser.wm_app + endpoint
        data = {
            "Cancelled": True,
            "MaximumStatus":9000,
            "MinimumStatus":9000
            }
        res = requests.put(url, headers=self.activeUser.headers, data=json.dumps(data))
        return response._response_handler(res)

    def cancel_original_order(self, original_order_id):
        endpoint = f"/dcorder/api/dcorder/originalOrder/originalOrderId/{original_order_id}"
        url = self.activeUser.wm_app + endpoint
        data = {
            "Cancelled": True
            }
        res = requests.put(url, headers=self.activeUser.headers, data=json.dumps(data))
        return response._response_handler(res)


    ##excel methods
    def export_excel_order(self):
        endpoint = '/dcorder/api/dcorder/order/exportExcel'
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._excel_response_handler(res)


    def import_excel_order(self, excelfile):
        endpoint = '/dcorder/api/dcorder/order/importExcel'
        url = self.activeUser.wm_app + endpoint
        files=[
            ('workbook',(excelfile, open(excelfile,'rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        ]
        del headers['Content-Type']
        res = requests.post(url, headers=self.activeUser.headers, data={}, files=files)
        return response._excel_response_handler(res)

    def export_excel_pipeline(self):
        endpoint =  '/dcorder/api/ServiceDefinition/pipeline/exportExcel'
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._excel_response_handler(res)

    def import_excel_pipeline(self, excelfile):
        endpoint =  '/dcorder/api/ServiceDefinition/pipeline/importExcel'
        url = self.activeUser.wm_app + endpoint
        files=[
            ('workbook',(excelfile, open(excelfile,'rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        ]
        del headers['Content-Type']
        res = requests.post(url, headers=self.activeUser.headers, data={}, files=files)
        return response._excel_response_handler(res)

        