import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from Google_Api.credentials.config import *

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
        print(SCOPES)

        cred = None

        pickle_file = os.path.join(os.path.dirname(__file__), 'credentials', f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle')
        print(pickle_file)

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
            print(cred)
            print(API_SERVICE_NAME, 'service created successfully')
            return service
        except Exception as e:
            print(e)
            print(
                f'Failed to create service instance for {API_SERVICE_NAME}')
            os.remove(pickle_file)
            return None
