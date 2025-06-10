import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.wtp import *

class Wiretap(Component):
    def __init__(self, activeUser):
        '''wiretap/api/wiretap'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services)
        super().__init__(activeUser, 'wiretap')