import uuid
import json
import unittest
import pandas as pd

try:
    from journal.aws_CRUD import AWS_CRUD_API
    from journal.config_file import *
except ModuleNotFoundError:
    from src.journal.aws_CRUD import AWS_CRUD_API
    from src.journal.config_file import *

# documentation for the DynamoDB table https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#table
print("Testing:" + AWS_CRUD_API.__doc__)

# keep the create client connection separate to ensure that a
# new connection is established after each tests

def create_client_connection():
    '''
    Returns an instance of an AWS_CRUD_API using the credentials from the config file
    '''
    return AWS_CRUD_API(
        AWS_ACCESS_KEY_ID,
        AWS_SECRET_ACCESS_KEY,
        AWS_REGION,
        DYNAMO_DB_NAME,
        S3_BUCKET_NAME
    )


class Test_AWS_CRUD_API(unittest.TestCase):

    def setUp(self):
        self.api = create_client_connection()
        self.fileIDs = []
        self.username = 'test-user'
        self.fileID_1 = self.username + "/" + uuid.uuid4().hex
        self.fileID_2 = self.username + "/" + uuid.uuid4().hex

    # test that our credentials are still valid and that the client can
    # connect to AWS with those new credentials
    def test_client_connection(self):
        client = create_client_connection()
        self.assertIsNotNone(client)

    # if the client return a list of files the user_files variable should be a
    # list of objects or an empty list
    def test_get_user_files(self):
        user_files = self.api.get_user_files(self.username)
        self.assertEqual(type(user_files), list)

    def test_create_user_files(self):

        # get initial user_files
        initial_user_files = self.api.get_user_files(self.username)

        # create two random data frames and save them to AWS
        self.api.create_user_file(
            self.username, self.fileID_1, 'test-file-1.csv', pd.DataFrame([1, 0, 7]).to_json())
        self.api.create_user_file(
            self.username, self.fileID_2, 'test-file-2.csv', pd.DataFrame([0, 0, 5]).to_json())

        # check that there are two more items in the database
        final_user_files = self.api.get_user_files(self.username)
        self.assertEqual(len(initial_user_files), len(final_user_files) - 2)

        # check that the file content is right
        selected_file = list(filter(lambda file: file["filename"] == 'test-file-2.csv', final_user_files))[0]
        self.assertEqual(json.loads(pd.DataFrame([0, 0, 5]).to_json())["0"], selected_file["file_content"]["0"])

    def test_delete_user_files(self):
        # get initial user_files
        initial_user_files = self.api.get_user_files(self.username)

        # create two random data frames and save them to AWS
        self.api.create_user_file(
            self.username, self.fileID_1, 'test-file-1.csv', pd.DataFrame([1, 0, 7]).to_json())

        # test the file that has just been created
        self.api.delete_user_file('test-file-1.csv', self.username)

        # check that there are two more items in the database
        final_user_files = self.api.get_user_files(self.username)
        self.assertEqual(len(initial_user_files), len(final_user_files))

    def tearDown(self):
        all_user_files = self.api.get_user_files(self.username)
        [self.api.delete_user_file(file["filename"], self.username)
         for file in all_user_files]


if __name__ == "__main__":
    unittest.main()
