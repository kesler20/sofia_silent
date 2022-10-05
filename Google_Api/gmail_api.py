import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
# for dealing with attachement MIME types
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from mimetypes import guess_type as guess_mime_type

# Request all access (permission to read/send/receive emails, manage the inbox, and more)

import logging
logging.basicConfig(
    filename=r"C:\Users\Uchek\Protocol\Sofia\logs_src\main_logs.log",
    level=logging.DEBUG,
    format='%(asctime)s:%(levelname)s:%(message)s)'
)

try:
    from Google_Api.google_api import GoogleApi
    from Google_Api.config_files.config_file import *
    from Google_Api.logs_google_api.google_api_logging import logger

except ModuleNotFoundError:
    def check_directory(path: str):
        if path.startswith('.') or path.startswith('__') or path.endswith('.exe'):
            return False
        else:
            return True
    _modules = list(filter(check_directory, os.listdir(os.getcwd())))
    for module in _modules:
        sys.path.append(os.path.join(os.getcwd(), module))
    logging.info('----------- Moduels in System Path ------------')
    logging.info(sys.path)

    from google_api import GoogleApi
    from config_files.config_file import *
    from logs_google_api.google_api_logging import logger

# FOR DOCUMENTATION WHICH WORKS https://www.thepythoncode.com/article/use-gmail-api-in-python


class GmailApi(GoogleApi):

    def __init__(self, client_secret_file, api_name, api_version, *scopes):
        super().__init__(client_secret_file, api_name, api_version, *scopes)

    # Adds the attachment with the given filename to the given message

    def add_attachment(self, message, filename):
        content_type, encoding = guess_mime_type(filename)
        if content_type is None or encoding is not None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        if main_type == 'text':
            fp = open(filename, 'rb')
            msg = MIMEText(fp.read().decode(), _subtype=sub_type)
            fp.close()
        elif main_type == 'image':
            fp = open(filename, 'rb')
            msg = MIMEImage(fp.read(), _subtype=sub_type)
            fp.close()
        elif main_type == 'audio':
            fp = open(filename, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=sub_type)
            fp.close()
        else:
            fp = open(filename, 'rb')
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(fp.read())
            fp.close()
        filename = os.path.basename(filename)
        msg.add_header('Content-Disposition', 'attachment', filename=filename)
        message.attach(msg)

    def build_message(self, our_email, destination, obj, body, attachments=[]):
        if not attachments:  # no attachments given
            message = MIMEText(body)
            message['to'] = destination
            message['from'] = our_email
            message['subject'] = obj
        else:
            message = MIMEMultipart()
            message['to'] = destination
            message['from'] = our_email
            message['subject'] = obj
            message.attach(MIMEText(body))
            for filename in attachments:
                self.add_attachment(message, filename)
        return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

    def send_email(self, message, recipient):
        service = self.Create_Service()
        email_msg = message
        mimeMessage = MIMEMultipart()
        mimeMessage['to'] = f'{recipient}@gmail.com'
        mimeMessage['subject'] = 'from Sofia'
        mimeMessage.attach(MIMEText(email_msg, 'plain'))
        raw_string = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()

        message = service.users().messages().send(
            userId='me', body={'raw': raw_string}).execute()
        logger.info(message)

    def search_messages(self, query):
        service = self.Create_Service()
        result = service.users().messages().list(userId='me', q=query).execute()
        messages = []
        if 'messages' in result:
            messages.extend(result['messages'])
        while 'nextPageToken' in result:
            page_token = result['nextPageToken']
            result = service.users().messages().list(
                userId='me', q=query, pageToken=page_token).execute()
            if 'messages' in result:
                messages.extend(result['messages'])
        return messages

    def delete_messages(self, query):
        # query can be the email id such as Google Alerts
        # it can also be the email of the sender
        service = self.Create_Service()
        messages_to_delete = self.search_messages(query)
        # it's possible to delete a single message with the delete API, like this:
        # service.users().messages().delete(userId='me', id=msg['id'])
        # but it's also possible to delete all the selected messages with one query, batchDelete
        return service.users().messages().batchDelete(
            userId='me',
            body={
                'ids': [msg['id'] for msg in messages_to_delete]
            }
        ).execute()


API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']
client_secret_file = CLIENT_SECRET_FILE

gmail_api = GmailApi(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

if __name__ == '__main__':
    emails_to_delete = ['global@admiralmarkets.com']

    for email in emails_to_delete:
        gmail_api.delete_messages(email)