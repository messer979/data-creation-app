import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.ptw import *

#transactions
class Putaway(Component):
    def __init__(self, activeUser):
        '''putaway/api/putaway'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services)
        super().__init__(activeUser, 'putaway')
        
    def load_task_dtls_by_locns(self, locationIds):
        endpoint = f"/putaway/api/putaway/common/taskDetails/byLocationIds"
        url = self.activeUser.wm_app + endpoint
        if type(locationIds) != str:
            locationIds = json.dumps(locationIds)
        res = requests.post(url, headers=self.activeUser.headers, data=locationIds)
        return response._response_handler(res)

    def load_tasks_by_stat(self, status):
        endpoint = f"/putaway/api/putaway/common/taskIdsByStatus/status/{status}"
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._response_handler(res)
