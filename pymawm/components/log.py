import requests
import json
from pymawm.resources import response
from pymawm.components.component_base import Component
from pymawm.services.log import *

class Log(Component):
    def __init__(self, activeUser):
        self.activeUser = activeUser
        self.methods = {}
        super().__init__(activeUser)
        self._load_logs()

    def _load_logs(self):
        for func_name, endpoint in log_services.items():
            self._create_log_method(func_name, endpoint)


    def _create_log_method(self, func_name, endpoint):
        new_func = f'''def {func_name}(self, log_level="DEBUG"):\n\t """\n\t desc\n\t """\n\t endpoint = '{endpoint}'+ log_level\n\t url = self.activeUser.wm_app + endpoint\n\t res = requests.post(url, headers=self.activeUser.headers)\n\t return response._response_handler(res, verboseheaders=self.activeUser.headers.verbose)'''
        self._exec_prepared_method(new_func, func_name)
