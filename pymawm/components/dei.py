import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.dei import *

class EquipmentIntegration(Component):
    def __init__(self, activeUser):
        '''device-integration/api/deviceintegration'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services)
        super().__init__(activeUser, 'device-integration')
        
    #import 
    def receive_message_at_endpoint(self, sourceEndpoint, data):
        endpoint = f'/device-integration/api/deviceintegration/process/{sourceEndpoint}'
        url = self.activeUser.wm_app + endpoint
        if type(data) == dict:
            data=json.dumps(data)
        res = requests.post(url, headers=self.activeUser.headers, data=data)
        return response._response_handler(res)

    def send(self, data):
        endpoint = f'/device-integration/api/deviceintegration/process'
        url = self.activeUser.wm_app + endpoint
        res = requests.post(url, headers=self.activeUser.headers, data=data)
        return res
        # return response._response_handler(res)

    def send_mhe(self, transport, message):
        endpoint = f'/device-integration/api/deviceintegration/process/{transport}'
        url = self.activeUser.wm_app + endpoint
        if type(message) == dict:
            message=json.dumps(message)
        res = requests.post(url, headers=self.activeUser.headers, data=message)
        return response._response_handler(res, verbose=self.activeUser.verbose)
