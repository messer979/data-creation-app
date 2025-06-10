import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component

class Misc(Component):
    def __init__(self, activeUser):
        self.activeUser = activeUser
        self.methods = {}
        super().__init__(activeUser)

    def get_ascii_docs(self, component):
        endpoint=f'/{component}/api/asciidoc'
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return res

    def get_service_def(self, component):
        endpoint=f'/{component}/api/ServiceDefinition/serviceDefinition?size=1'
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return res

