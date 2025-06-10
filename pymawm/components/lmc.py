from pymawm.components.component_base import Component
from pymawm.services.lmc import *

#transactions
class LMCore(Component):
    def __init__(self, activeUser):
        '''lmcore/api/lmcore'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services)
        super().__init__(activeUser, 'lmcore')