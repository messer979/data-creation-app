import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.dcl import *

#transactions
class DCLayout(Component):
    def __init__(self, activeUser):
        '''dclayout/api/dclayout'''
        self.activeUser = activeUser
        self.methods = dict(general_services=general_services, import_services=import_services, get_services=get_services)
        super().__init__(activeUser, 'dclayout')