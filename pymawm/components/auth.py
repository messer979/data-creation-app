import requests
# from urllib.parse import quote
import logging
logger = logging.getLogger(__name__)

def auth(user, password, auth_app):
    endpoint = '/oauth/token'
    url = auth_app + endpoint
    payload = {
        "grant_type":"password",
        "username":user,
        "password":password
        }
    headers = {
        'Authorization': 'Basic b21uaWNvbXBvbmVudC4xLjAuMDpiNHM4cmdUeWc1NVhZTnVu',
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload, verify=True)
    except Exception as e:
        logger.error(e)
        response = ''
    return response