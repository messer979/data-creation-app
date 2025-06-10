import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.aud import *

#transactions
class Audit(Component):
    '''audit/api/audit'''
    def __init__(self, activeUser):
        self.activeUser = activeUser
        self.methods = dict(import_services=import_services)
        super().__init__(activeUser, 'audit')