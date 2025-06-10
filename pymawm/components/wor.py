import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.wor import *

class WorkRelease(Component):
    def __init__(self, activeUser):
        '''workrelease/api/workrelease'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, general_services=general_services)
        super().__init__(activeUser, 'workrelease')