import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.tsk import *

class Task(Component):
    def __init__(self, activeUser):
        '''task/api/task'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services)
        super().__init__(activeUser, 'task')
        
    def determine_eligible_task_path(self, task_path_request):
        endpoint = "/task/api/task/path/eligibility"
        url = self.activeUser.wm_app + endpoint
        if type(task_path_request) == str:
            task_path_request = json.dumps(task_path_request)
        res = requests.post(url, headers=self.activeUser.headers, data=task_path_request)
        return response._response_handler(res)    

    def determine_task_path_for_task(self, task):
        endpoint = f"/task/api/task/taskPath/eligibility/taskId/{task}"
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._response_handler(res)

    def determine_task_path_for_task_seq(self, task, sequence):
        endpoint = f"task/api/task/taskPath/eligibility/taskId/{taskId}/sequence/{sequence}"
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._response_handler(res)


    def get_user_eligible_zones(self, SourceLocationId, TransactionId, TransactionTypeId):
        endpoint = f"task/api/task/userEligibleZones"
        url = self.activeUser.wm_app + endpoint
        params = dict(SourceLocationId=SourceLocationId, TransactionId=TransactionId, TransactionTypeId=TransactionTypeId)
        res = requests.get(url, headers=self.activeUser.headers, params=params)
        return response._response_handler(res)
