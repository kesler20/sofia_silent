import pandas as pd
import datetime
from Google_Api.credentials.config import *
from Google_Api.google_api import GoogleApi


class TasksApi(GoogleApi):

    def __init__(self, client_secret_file, api_name, api_version, *scopes):
        super().__init__(client_secret_file, api_name, api_version, *scopes)

    def convert_to_RFC_datetime(self, year=1900, month=1, day=1, hour=0, minute=0):
        dt = datetime.datetime(year, month, day, hour,
                               minute, 0, 000).isoformat() + 'Z'
        return dt

    """
    Initialize response
    """

    def construct_service_and_response_for_tasklists(self):
        service = self.Create_Service()
        response = service.tasklists().list().execute()
        return service, response

    def construct_service_and_response_for_tasks(self, index_of_main_tasklists):
        API_NAME = 'tasks'
        API_VERSION = 'v1'
        SCOPES = ["https://www.googleapis.com/auth/tasks"]
        service = self.Create_Service()
        servc, respns = self.construct_service_and_response_for_tasklists()
        Tasklist = respns.get('items')[index_of_main_tasklists]['id']
        response = service.tasks().list(
            tasklist=Tasklist
        ).execute()
        return service, response
    """
    Insert Method
    """

    def construct_request_body(self, title, notes=None, due=None, status='needsAction', deleted=False):
        try:
            request_body = {
                'title': title,
                'notes': notes,
                'due': due,
                'deleted': deleted,
                'status': status
            }
            return request_body
        except Exception:
            return None

    def insert_tasklist(self, title, index_of_main_tasklists, notes, dt):
        service, response = self.construct_service_and_response_for_tasklists()
        Tasklist = response.get('items')[index_of_main_tasklists]
        TasklistId = Tasklist['id']
        new_task_response = service.tasklists().insert(
            body=self.construct_request_body(title, notes=notes, due=dt),
        ).execute()
        print(new_task_response)

    def insert_task_to_tasklist(self, title, index_of_main_tasklists, notes, dt):
        service, response = self.construct_service_and_response_for_tasklists()
        Tasklist = response.get('items')[index_of_main_tasklists]
        TasklistId = Tasklist['id']
        new_task_response = service.tasks().insert(
            body=self.construct_request_body(title, notes=notes, due=dt),
            tasklist=TasklistId
        ).execute()
        print(new_task_response)

    def update_main_task_title(self, index, title):
        service, response = self.construct_service_and_response_for_tasklists()
        Tasklist = response.get('items')[index]
        print(Tasklist)
        Tasklist['title'] = title
        service.tasklists().update(
            tasklist=Tasklist['id'], body=Tasklist).execute()

    """
    List Method
    """
    dt_Max = convert_to_RFC_datetime(2022, 5, 1)

    def list_tasks_due_dt(self, index_of_main_tasklists, dt_Max):
        service, response = self.construct_service_and_response_for_tasklists()
        Tasklist = response.get('items')[index_of_main_tasklists]
        TasklistId = Tasklist['id']

        response = service.tasks().list(
            tasklist=TasklistId,
            dueMax=dt_Max,
            showCompleted=False
        ).execute()
        lstItems = response.get('items')
        nextPageToken = response.get('nextPageToken')
        print(pd.DataFrame(lstItems))

    """
        Delete Method
        isinstance(int(item.get('title').replace('Tasklst #', '')), int):
        int(item.get('title').replace('Tasklst #', '')) > 50:
        service.tasklists().delete(tasklist=item.get('id')).execute()
    """

    def delete_tasklists(self, index_of_main_tasklists):
        service, response = self.construct_service_and_response_for_tasklists()
        Tasklist = response.get('items')[index_of_main_tasklists]
        TasklistId = Tasklist['id']
        new_task_response = service.tasklists().delete(
            tasklist=TasklistId
        ).execute()
        print(new_task_response)

    def delete_tasks(self, index_of_main_tasklists, index_of_main_tasks):
        service0, response0 = self.construct_service_and_response_for_tasklists()
        Tasklist0 = response0.get('items')[index_of_main_tasklists]
        TasklistId0 = Tasklist0['id']
        service, response = self.construct_service_and_response_for_tasks(
            index_of_main_tasklists)
        Tasklist = response.get('items')[index_of_main_tasks]
        TasklistId = Tasklist['id']
        new_task_response = service.tasks().delete(
            tasklist=TasklistId0,
            task=TasklistId
        ).execute()
        print(new_task_response)


API_NAME = 'tasks'
API_VERSION = 'v1'
SCOPES = ["https://www.googleapis.com/auth/tasks"]
task_api = TasksApi(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
