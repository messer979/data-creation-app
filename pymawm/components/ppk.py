import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.ppk import *

#transactions
class PickPack(Component):
    def __init__(self, activeUser):
        '''/pickpack/api/pickpack'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services, import_services=import_services)
        super().__init__(activeUser, 'pickpack')