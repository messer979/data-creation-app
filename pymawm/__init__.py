from pymawm.components.alt import AlertNotification
from pymawm.components.apt import Appointment
from pymawm.components.aud import Audit
from pymawm.components.aux_ import Auxsvcs
from pymawm.components.auth import auth
from pymawm.components.car import Carrier
from pymawm.components.cfs import ConfigStore
from pymawm.components.dca import Allocation
from pymawm.components.cub import Cubing
from pymawm.components.cut import Commonutil
from pymawm.components.dcc import DCConsolidation
from pymawm.components.dcl import DCLayout
from pymawm.components.dco import Dco
from pymawm.components.dcs import DCShipping
from pymawm.components.dci import DCInv
from pymawm.components.dei import EquipmentIntegration
from pymawm.components.dmu import DMUIFacade
from pymawm.components.dms import DMUISearch
from pymawm.components.eml import Email
from pymawm.components.fac import Facility
from pymawm.components.inm import InvMgmt
from pymawm.components.itm import Item
from pymawm.components.log import Log
from pymawm.components.lmc import LMCore
from pymawm.components.lpd import LpnDisposition
from pymawm.components.mis import Misc
from pymawm.components.org import Org
from pymawm.components.pcl import Parcel
from pymawm.components.pix import Pix
from pymawm.components.ppk import PickPack
from pymawm.components.ptw import Putaway
from pymawm.components.rcv import Recv
from pymawm.components.rf import Rf
from pymawm.components.rtg import Rtg
from pymawm.components.shp import Shipment
from pymawm.components.slo import Slotting
from pymawm.components.shc import ShipConfirm
from pymawm.components.tsk import Task
from pymawm.components.ven import Vendor
from pymawm.components.wor import WorkRelease
from pymawm.components.wtp import Wiretap
from pymawm.components.xnt import Xint
from pymawm.components.yms import Yms

from pymawm.automation.data_extracts import Extract

from pymawm.components.component_base import Component
from pymawm.resources.tools import ActiveTools

import logging
logger = logging.getLogger(__name__)
# logging.basicConfig(level="INFO")

import threading
import inspect

class ActiveWM(object):
    #must specifify either authserver or auth_port. Port is used when an environment is on one machine only, server is used when across many machines. Typically, authserver should be used.
    def __init__(self, username='', password='', environment='', authserver=None, auth_port='', app_port='', default_facility='', default_org='', manual_token=''):
        self.verbose = True
        self.logged_in = False
        self.username = username
        self.password = password
        self.current_facility = default_facility
        self.manual_token = manual_token
        if auth_port != '':
            self.auth_app = environment + ':' + auth_port
        else:
            self.auth_app = authserver
        if app_port != '':
            self.wm_app = environment + ':' + app_port
        else:
            self.wm_app = environment
        ## org required as of new auth changes 
        self.organization = default_org
        self.login()
        self._add_submodules()
        self.full_comp_list = ['appointment', 'asset-manager', 'aux-svcs', 'carrier', 'commonui-facade', 'commonutil', 'configstore', 'cfg', 'controller', 'cubing', 'dcallocation', 'dcconsolidation', 'dcinventory', 'dclayout', 'dcorder', 'dcshipping', 'device-integration', 'distancetime', 'dmmobile-facade', 'dmui-facade', 'dmui-search', 'edge-router', 'elasticsearch', 'facility', 'feasibility', 'fwuifacade', 'geo', 'inventory-management', 'item-master', 'lane-manager', 'lmcore', 'lmincentivepay', 'lminteraction', 'lpn-disposition', 'markmagic', 'messenger', 'organization', 'pickpack', 'pix', 'print-config', 'proactive', 'putaway', 'receiving', 'rf-config', 'routing', 'scheduler', 'shipconfirm', 'shipment', 'slotting', 'spe', 'task', 'tms-search', 'tmsui-facade', 'vendor', 'wiretap', 'workrelease', 'xboundauth', 'xint', 'yard-management']
        self.comp_registry = [key for key, val in self.__dict__.items() if issubclass(val.__class__,Component)]
        if self.logged_in:
            self.headers = {
                'Content-Type': 'application/json',
                'User-Agent' : 'pymawm',
                'Authorization': self.token,
                'Location' : self.current_facility,
                'Organization' : self.organization
            }
        else:
            self.headers = {
                'Content-Type': 'application/json',
                'User-Agent' : 'pymawm',
                'Authorization': '',
                'Location' : '',
                'Organization' : ''
            }
    def __repr__(self):
        return f"{type(self).__name__}(wm_app='{self.wm_app}', user={self.username}, facility={self.current_facility})"

    def login(self):
        if self.manual_token != '':
            self.token = self.manual_token
            if not self.token.lower().startswith("bearer "):
                self.token = "Bearer " + self.token
            self.logged_in = True
            logger.info(f'skipped auth cause we have a token already {self.token}')
            return
        try:
            self.auth_response = auth(self.username, self.password, self.auth_app)
        except Exception as e:
            logger.error('Failed to connect to server')
            logger.error(e)
        try:
            self.token = "bearer " + self.auth_response.json()['access_token']
            logger.info('Token Obtained: ' + self.token)
            self.logged_in = True
        except Exception as e:
            self.token = None
            logger.error('Failed to get token.')
            logger.exception("error")
    
    def _add_submodules(self):
        self.alt = AlertNotification(self)
        self.apt = Appointment(self)
        self.aud = Audit(self)
        self.aux = Auxsvcs(self)
        self.dca = Allocation(self)
        self.car = Carrier(self)
        self.cfs = ConfigStore(self)
        self.cub = Cubing(self)
        self.cut = Commonutil(self)
        self.dcc = DCConsolidation(self)
        self.dcl = DCLayout(self)
        self.dci = DCInv(self)
        self.dco = Dco(self)
        self.dcs = DCShipping(self)
        self.dei = EquipmentIntegration(self)
        self.dmu = DMUIFacade(self)
        self.dms = DMUISearch(self)
        self.eml = Email(self)
        self.fac = Facility(self)
        self.inm = InvMgmt(self)
        self.itm = Item(self)
        self.log = Log(self)
        self.lmc = LMCore(self)
        self.lpd = LpnDisposition(self)
        self.mis = Misc(self)
        self.org = Org(self)
        self.pcl = Parcel(self)
        self.ppk = PickPack(self)
        self.pix = Pix(self)
        self.ptw = Putaway(self)
        self.rcv = Recv(self)
        self.rf  = Rf(self)
        self.rtg  = Rtg(self)
        self.shp = Shipment(self)
        self.shc = ShipConfirm(self)
        self.slo = Slotting(self)
        self.tsk = Task(self)
        self.ven = Vendor(self)
        self.wor = WorkRelease(self)
        self.wtp = Wiretap(self)
        self.xnt = Xint(self)
        self.yms = Yms(self)
        self.extract = Extract(self)

    def comps(self):
        '''prints out the list of components'''
        comp_list = []
        for comp, obj in vars(self).items():
            if issubclass(type(obj), Component):
                print(comp)
                comp_list.append(comp)
        return comp_list

    def wakeup(self):
        '''makes request from every component to turn them on'''
        self.verbose = False
        down_comps = []
        logger.setLevel("INFO")
        logger.info(f"Starting wakeup process")
        for comp in self.full_comp_list:
            res = self.mis.get_service_def(comp)
            logger.info(f"{comp} responded with {res}")
            if res.status_code == 500:
                down_comps.append(comp)
        logger.info(f"\nFollowing components are down: {', '.join(down_comps)}")
        self.verbose = True
        logger.setLevel("ERROR")

    def wakeup_p(self):
        '''makes request from every component to turn them on'''
        self.verbose = False
        down_comps = []
        for comp in self.full_comp_list:
            res = self.mis.get_service_def(comp)
            print(comp, res)
            if res.status_code == 500:
                down_comps.append(comp)
        print(f"\nFollowing components are down: {', '.join(down_comps)}")
        self.verbose = True

    def threaded_wakeup(self):
        thread = threading.Thread(target=self.wakeup)
        thread.start()

    def service_override(self, comp_service_dict:dict) -> None:
        for comp, service_types in comp_service_dict.items():
            if comp in self.comp_registry:
                comp_to_override = getattr(self, comp)
                comp_to_override.run_override(service_types)
            else:
                logger.info(f'{comp} not in registry')

class ActiveWMTemplate(object):
    def __init__(self):
        self.alt = AlertNotification(self)
        self.apt = Appointment(self)
        self.aud = Audit(self)
        self.aux = Auxsvcs(self)
        self.dca = Allocation(self)
        self.car = Carrier(self)
        self.cfs = ConfigStore(self)
        self.cub = Cubing(self)
        self.cut = Commonutil(self)
        self.dcc = DCConsolidation(self)
        self.dcl = DCLayout(self)
        self.dci = DCInv(self)
        self.dco = Dco(self)
        self.dcs = DCShipping(self)
        self.dei = EquipmentIntegration(self)
        self.dmu = DMUIFacade(self)
        self.dms = DMUISearch(self)
        self.eml = Email(self)
        self.fac = Facility(self)
        self.inm = InvMgmt(self)
        self.itm = Item(self)
        self.log = Log(self)
        self.lmc = LMCore(self)
        self.lpd = LpnDisposition(self)
        self.mis = Misc(self)
        self.org = Org(self)
        self.pcl = Parcel(self)
        self.ppk = PickPack(self)
        self.pix = Pix(self)
        self.ptw = Putaway(self)
        self.rcv = Recv(self)
        self.rf  = Rf(self)
        self.rtg  = Rtg(self)
        self.shp = Shipment(self)
        self.shc = ShipConfirm(self)
        self.slo = Slotting(self)
        self.tsk = Task(self)
        self.ven = Vendor(self)
        self.wor = WorkRelease(self)
        self.wtp = Wiretap(self)
        self.xnt = Xint(self)
        self.yms = Yms(self)
        self.extract = Extract(self)
