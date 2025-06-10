import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.rtg import *

class Rtg(Component):
    def __init__(self, activeUser):
        '''routing/api/routing'''
        self.activeUser = activeUser
        self.methods = dict(general_services=general_services)
        super().__init__(activeUser, 'routing')