import requests
import json
from pymawm.resources import response, complex_query
#from pymawm.tools import cycle_count_tools
from pymawm.components.component_base import Component
from pymawm.services.inm import *

#transactions
class InvMgmt(Component):
    def __init__(self, activeUser):
        '''inventory-management/api/inventory-management'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services)
        super().__init__(activeUser, 'inventory-management')