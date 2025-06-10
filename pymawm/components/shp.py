import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.shp import *

#transactions
class Shipment(Component):
    def __init__(self, activeUser):
        '''/shipment/api/shipment'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services)
        super().__init__(activeUser, 'shipment')