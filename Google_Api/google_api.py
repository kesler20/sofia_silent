import pickle
import os
import sys
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import logging 

logging.basicConfig(
    filename=r'"C:\Users\Uchek\Protocol\Sofia\logs_src\main_logs.log"',
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s)'
)

try:
    from Google_Api.config_files.config_file import *
    from Google_Api.logs_google_api.google_api_logging import logger

except ModuleNotFoundError:
    def check_directory(path: str):
        if path.startswith('.') or path.startswith('__') or path.endswith('.exe'):
            return False
        else:
            return True
    _modules = list(filter(check_directory,os.listdir(os.getcwd())))
    for module in _modules:
        sys.path.append(os.path.join(os.getcwd(),module))
    logging.info('----------- Modules in System Path ------------')
    logging.info(sys.path)

    from config_files.config_file import *
    from logs_google_api.google_api_logging import logger

'''
    link to the api documentation can be found at https://developers.google.com/tasks
    refresh the token on the link below if you dont have permission switch to uchekesla account 
    donwload json and update secret_file 
    delete the pickle file that you have created
    and to renew credentials go to https://console.cloud.google.com/apis/credentials?authuser=1&project=learned-vault-319419 
'''

class GoogleApi(object):

    def __init__(self, client_secret_file, api_name, api_version, *scopes):
        self.client_secret_file = client_secret_file
        self.api_name = api_name
        self.api_version = api_version
        self.scopes = scopes

    def Create_Service(self):

        CLIENT_SECRET_FILE = self.client_secret_file
        API_SERVICE_NAME = self.api_name
        API_VERSION = self.api_version
        SCOPES = [scope for scope in self.scopes[0]]
        logger.info(SCOPES)

        cred = None

        pickle_file = os.path.join(os.path.dirname(__file__),'config_files',f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle')
        logger.info(pickle_file)

        if os.path.exists(pickle_file):
            with open(pickle_file, 'rb') as token:
                cred = pickle.load(token)

        if not cred or not cred.valid:
            if cred and cred.expired and cred.refresh_token:
                cred.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CLIENT_SECRET_FILE, SCOPES
                )
                cred = flow.run_local_server()

            with open(pickle_file, 'wb') as token:
                pickle.dump(cred, token)

        try:
            service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
            logger.info(cred)
            logger.info(API_SERVICE_NAME, 'service created successfully')
            return service
        except Exception as e:
            logger.info(e)
            logger.info(
                f'Failed to create service instance for {API_SERVICE_NAME}')
            os.remove(pickle_file)
            return None
