import requests
import json
from pymawm.resources import response, complex_query
from pymawm.components.component_base import Component
from pymawm.services.org import *

class Org(Component):
    def __init__(self, activeUser):
        '''/organization/api/organization'''
        self.activeUser = activeUser
        self.methods = dict(search_services=search_services, get_services=get_services, general_services=general_services)
        super().__init__(activeUser, 'organization')
        
    #search methods
    def quick_get(self, service, **kwargs):
        endpoint = f"/organization/api/organization/{service}"
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._response_handler(res)

    def quick_search_UserId(self, user):
        endpoint = f'/organization/api/organization/user/search'
        url = self.activeUser.wm_app + endpoint
        query = {
            "Query": f"UserId~{user}"
            }
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(query))
        return response._response_handler(res)

    def quick_search_RoleId(activerUser, role_id):
        endpoint = f'/organization/api/organization/role/search'
        url = self.activeUser.wm_app + endpoint
        payload = {
            "Query": f"RoleId~{role_id}"
            }
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(payload))
        return response._response_handler(res)

    def set_password(self, newpassword):
        endpoint = '/organization/api/organization/user/updatePassword'
        url = self.activeUser.wm_app + endpoint
        payload = { 
            "UserId": self.username, 
            "CurrentPassword": self.password, 
            "NewPassword" : newpassword
        }
        res = requests.post(url, headers=self.activeUser.headers, data = json.dumps(payload))
        if res.status_code == '200':
            self.password = newpassword
        return response._response_handler(res)

    def change_password_policy(self, pk, ord_id, new_config={}):
        endpoint = f'/organization/api/organization/passwordPolicyConfig/{PK}'
        url = self.activeUser.wm_app + endpoint
        if new_config == {}:
            payload = {
                'AllowConsecutiveIdenticalChars': True,
                'AllowPasswordIdenticalToUserId': True,
                'LowercaseRequired': True,
                'Messages': None,
                'MinimumPasswordLength': 4,
                'NotifyPasswordExpiringDays': '5',
                'NumberRequired': False,
                'OrganizationId': self.activeUser.organization,
                'PasswordExpiration': 365,
                'Process': None,
                'ResetPasswordExpiration': 1,
                'SpecialCharacterRequired': False,
                'UppercaseRequired': False
            }
        else:
            new_config = payload
        policy = PasswordPolicy(**new_config)
        res = requests.put(url, headers=self.activeUser.headers, data=policy.convertForImport())
        return response._response_handler(res)

    def create_password_policy(self, policy):
        endpoint = '/organization/api/organization/passwordPolicyConfig'
        url = self.activeUser.wm_app + endpoint
        new_policy = PasswordPolicy(**policy)
        res = requests.post(url, headers=self.activeUser.headers, data=new_policy.convertForImport())
        return response._response_handler(res)


    def change_password_for_user(self, new_password):
        endpoint = '/organization/api/organization/user/updatePassword'
        url = self.activeUser.wm_app + endpoint
        payload = {
                    "UserId": self.username, 
                    "CurrentPassword": self.password, 
                    "NewPassword" : new_password
                }
        res = requests.post(url, headers=self.activeUser.headers, data=json.dumps(payload))
        return response._response_handler(res)


    def cleanedOrg(org_object, copied_user_data, new_user):
        org_to_copy = org_object[0]
        org = [{
            'OrganizationId': org_to_copy['OrganizationId'],
            'CreatedBy' : copied_user_data['UserId'],
            'UserId' : new_user.UserId,
            'UserRole' : [{
                'OrganizationId': org_to_copy['OrganizationId'],
                'RoleId' : org_to_copy['UserRole'][0]['RoleId'],
                'RoleOrgId' : org_to_copy['OrganizationId'],
                'UserId' : new_user.UserId
            }]
        }]
        return org

    def cleanedLocation(userLocation):
        del userLocation[0]['ContextId']
        del userLocation[0]['CreatedBy']
        del userLocation[0]['CreatedTimestamp']
        del userLocation[0]['PK']
        del userLocation[0]['ParentUser']
        del userLocation[0]['Process']
        del userLocation[0]['Unique_Identifier']
        del userLocation[0]['UpdatedBy']
        del userLocation[0]['UpdatedTimestamp']
        return userLocation

    def create_users_from_copy(self, user_to_copy, list_of_users):
        copied_user_data = search_user(self.activeUser, user_to_copy)['data'][0]
        org = copied_user_data['OrgUser']
        userLocale = copied_user_data['UserLocale']
        primaryOrgId = copied_user_data['PrimaryOrgId']
        userLocation = cleanedLocation(copied_user_data['UserLocation'])
        for user in list_of_users:
            new_user = User(**user)
            new_user.UserLocale = userLocale
            new_user.PrimaryOrgId = primaryOrgId
            new_user.UserLocation = userLocation
            new_user.OrgUser = cleanedOrg(org, copied_user_data, new_user)
            res = create_user(self, new_user)
            if res.status_code != 200:
                print(res.json())

    def send_password_reset(self, user):
        endpoint = f'/organization/api/organization/user/forgotpassword/{user}'
        url = self.activeUser.wm_app + endpoint
        res = requests.post(url, headers=self.activeUser.headers)
        return response._response_handler(res)


    def get_excel_export(self):
        endpoint = '/organization/api/organization/user/exportExcel'
        url = self.activeUser.wm_app + endpoint
        res = requests.get(url, headers=self.activeUser.headers)
        return response._excel_response_handler(res)


    def post_excel_export(self, excelfile):
        endpoint = '/organization/api/organization/user/importExcel'
        url = self.activeUser.wm_app + endpoint
        files=[
            ('workbook',('upload.xlsx',open(excelfile,'rb'),'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'))
        ]
        res = requests.post(url, headers=self.activeUser.headers, data={}, files=files)
        return response._excel_response_handler(res)