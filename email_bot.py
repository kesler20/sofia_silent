from bs4 import BeautifulSoup
from imaplib import IMAP4_SSL
# the documentation can be found at https://docs.python.org/3/library/imaplib.html
import email
from email.header import decode_header

'''The Email Bot can be sued to manipulate any email accounts without authentication 
'''
class EmailBot(object):

    def __init__(self,username, password, company_host='gmail.com'):
        self.username = username
        self.password = password
        self.company_host = f"imap.{company_host}"


# TODO: add functionality https://www.pythonpool.com/imap-python/#:~:text=Python%E2%80%99s%20client-side%20library%20called%20imaplib%20is%20used%20for,module%20defines%20three%20classes%2C%20IMAP4%2C%20IMAP4_SSL%2C%20and%20IMAP4_stream.
# account credentials
username = "uchekesla@gmail.com"
# generate a password from this link
# https://myaccount.google.com/apppasswords?rapt=AEjHL4OQy4SVJojZzGfvkRcLm4s-eBomRZ-g8DC3BQ6l7yg5L_pVm-OYoFEHaHmYMb18V1ZjnABZRWkJXbFybVmh4PJhdmQTdA
password = "gzbipxojfncswfiu"


# create an IMAP4 class with SSL
imap = IMAP4_SSL("imap.gmail.com")
# authenticate
imap.login(username, password)
# select inbox to avoid error -> command SEARCH illegal in state AUTH, only allowed in states SELECTED
imap.select("INBOX")
# search for specific mails by sender
# status, messages = imap.search(None, 'FROM "googlealerts-noreply@google.com"')
# to get mails by subject
# status, messages = imap.search(None, 'SUBJECT "Thanks for Subscribing to our Newsletter !"')
# to get all mails
# status, messages = imap.search(None, "ALL")
# to get mails after a specific date
status, messages = imap.search(None, 'SINCE "01-JAN-2020"')
# to get mails before a specific date
# email_subject = f'SUBJECT "Wednesday Footy 4-5"'
# print(email_subject)
# status, messages = imap.search(None, email_subject)
# status, messages = imap.search(None, 'BEFORE "01-JAN-2020"')
# convert messages to a list of email IDs
# from a specific email
# status, messages= imap.search(None, 'FROM contact@quantinsti.com')
messages = messages[0].split(b' ')
for mail in messages:
    _, msg = imap.fetch(mail, "(RFC822)")
    _, data = imap.fetch(mail, "(UID BODY[TEXT])")
    _, _from = imap.fetch(mail, "(BODY[HEADER.FIELDS (FROM)])")
    # for response in data:
    #     if isinstance(response, tuple):
    #         data = email.message_from_bytes(response[1])
    #         print(BeautifulSoup(data.as_string()).get_text())
    for response in _from:
        if isinstance(response, tuple):
            _from = email.message_from_bytes(response[1])
            print('from', _from['FROM'])
    # you can delete the for loop for performance if you have a long list of emails
    # because it is only for printing the SUBJECT of target email to delete
    for response in msg:
        if isinstance(response, tuple):
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                # if it's a bytes type, decode to str
                try:
                    subject = subject.decode()
                except UnicodeDecodeError:
                    pass
            print("Deleting", subject)
    # deleting mails
    imap.store(mail, "+FLAGS", "\\Deleted")


# permanently remove mails that are marked as deleted
# from the selected mailbox (in this case, INBOX)
# imap.expunge()
# close the mailbox
imap.close()
# logout from the account
imap.logout()
