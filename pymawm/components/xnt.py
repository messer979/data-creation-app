from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.xnt import *
from pymawm.templates.xnt import tranlog_summary_request_template

class Xint(Component):
    def __init__(self, activeUser):
        self.activeUser = activeUser
        self.methods = dict(general_services=general_services)
        super().__init__(activeUser, 'xint')

    def import_tran_log_request(self, data):
        if type(data) == dict:
            data = json.dumps(data, indent=4)
        tranlog_summary_request_template.update(data)
        url = self.activeUser.wm_app + endpoint
        res = requests.post(url, headers=self.activeUser.headers, data=data)
        return response._response_handler(res, verbose=self.activeUser.verbose)