import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.car import *

#transactions
class Carrier(Component):
    '''carrier/api/carrier'''
    def __init__(self, activeUser):
        self.activeUser = activeUser
        self.methods = dict(general_services=general_services)
        super().__init__(activeUser, 'carrier')