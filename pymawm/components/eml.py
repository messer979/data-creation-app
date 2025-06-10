import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.eml import *

#transactions
class Email(Component):
    def __init__(self, activeUser):
        '''email/api/email'''
        self.activeUser = activeUser
        self.methods = dict(general_services=general_services)
        super().__init__(activeUser, 'email')
