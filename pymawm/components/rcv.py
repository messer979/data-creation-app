import requests
import json
import base64
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.rcv import *

# def create_asns_from_csv(asns, asnLines):
class Recv(Component):
    def __init__(self, activeUser):
        '''receiving/api/receiving'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services)
        super().__init__(activeUser, 'receiving')


    def quick_search_asn(self, asn):
        endpoint = "/receiving/api/receiving/asn/search"
        url = self.activeUser.wm_app + endpoint
        query = {
            "Query": f"AsnId~{asn}"
            }
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(query))
        return response._response_handler(res)

    ## download methods
    def quick_get(self, service, **kwargs):
        endpoint = f"/receiving/api/receiving/{service}"
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._response_handler(res)

    ##delete methods
    def delete_asn_line_attribute_pk(self, pk):
        endpoint = f"/receiving/api/receiving/asnLineAttribute/{pk}"
        url = self.activeUser.wm_app + endpoint
        res = requests.delete(url, headers=self.activeUser.headers)
        return response._response_handler(res)

    def receive_lpn(self):
        endpoint = "/receiving/api/receiving/lpn/receive"
        url = self.activeUser.wm_app + endpoint
        return response._response_handler(res)

    ## excel methods
    def get_excel_export(self):
        endpoint = '/receiving/api/receiving/asn/exportExcel'
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        if res.status_code == 200:
            return base64.b64decode(res.json()['data'])
        else:
            print('error encountered')
            return res


    def post_excel_export(self, excelfile):
        endpoint = '/receiving/api/receiving/asn/importExcel'
        url = self.activeUser.wm_app + endpoint        
        files=[
            ('workbook',('out.xlsx',open(excelfile,'rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        ]
        res = requests.post(url, headers=self.activeUser.headers, data={}, files=files)
        if res.status_code == 200:
            return base64.b64decode(res.json()['data'])
        else:
            print('error encountered')
            return res