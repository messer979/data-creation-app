import requests
import json
import base64
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.dca import *

class Allocation(Component):
    def __init__(self, activeUser):
        '''dcallocation/api/dcallocation'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services)
        super().__init__(activeUser, 'dcallocation')