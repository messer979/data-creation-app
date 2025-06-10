import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component

class Rf(Component):
    def __init__(self, activeUser):
        '''rf-config/api/rf-config'''
        self.activeUser = activeUser
        self.methods = {}
        super().__init__(activeUser, 'rf-config')

    def get_ctrl_keys(self):
        url = self.activeUser.wm_app + endpoint
        True
