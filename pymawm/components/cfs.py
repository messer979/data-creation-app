from pymawm.components.component_base import Component
from pymawm.services.cfs import *

#transactions
class ConfigStore(Component):
    '''configstore/api/configstore'''
    def __init__(self, activeUser):
        self.activeUser = activeUser
        self.methods = dict(general_services=general_services)
        super().__init__(activeUser, 'configstore')