#!/usr/bin/env python

import re
from datetime import date
import httplib2
import os
from apiclient import discovery, errors
from oauth2client import client, tools
from oauth2client.file import Storage
import base64
import argparse

from pipe.src.message_factory import MessageFactory


class HarvestGmail:
    def __init__(self):
        # If modified, delete previously saved credentials at ~/.credentials/gmail-credentials.json
        self.scopes = 'https://www.googleapis.com/auth/gmail.modify'
        self.client_secret_file = '/Users/essvee/Documents/Project/Pipe/pipe/src/client_secret.json'
        self.application_name = 'DCP Pipeline'

    def main(self):
        """Runs class logic: controls flow of authentication,
        message retrieval and inbox updates.

        :return: List of Messages constructed by MessageFactory.
        These messages have been retrieved from the Gmail inbox
        and parsed to extract metadata.
        """
        # Get authenticated Gmail Service Object
        service = self.get_credentials()

        # Retrieve list of ids of unread emails
        unread_emails = self.list_unread_emails(service)

        # List to hold gapi_emails
        message_objects = []
        date_harvested = date.today()

        if unread_emails:
            print(f"Starting harvest. {len(unread_emails)} new emails found...")
            # Parse each email and send to MessageFactory for construction of message list
            for n in unread_emails:
                email_id, label, date_sent, email_body = self.email_metadata(service, n)
                messages = MessageFactory(email_id=email_id, label_id=label, sent_date=date_sent,
                                          email_body=email_body, source='GS', harvested_date=date_harvested).main()

                message_objects.extend(messages)

            # Mark emails as read
            self.mark_read(service, unread_emails)

        print(f"{len(message_objects)} new emails found.")
        return message_objects

    def email_metadata(self, service, email):
        """Parses Service objects and extracts first level of metadata.
        :param service: Gmail Service object
        :param email: ID of unread email
        :return: Tuple containing (email ID, label string, date email received, decoded email body).
        """
        # Retrieve full-text email using message_id
        full_email = self.get_email_full(service, email['id'])
        email_id = full_email['id']

        # Extract custom labels, received date and email body
        label = self.get_label(full_email)
        # Convert from internal date format
        date_received = date.fromtimestamp(int(full_email['internalDate']) / 1000).isoformat()
        email_body = base64.urlsafe_b64decode(full_email['payload']['body'].get('data') or None)

        return email_id, label, date_received, email_body

    def get_credentials(self):
        """Gets user credentials from storage.
        If credentials not found or invalid, the OAuth2 flow
        is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
            :return: Gmail Service object
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')

        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'gmail-credentials.json')
        store = Storage(credential_path)
        credentials = store.get()
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(self.client_secret_file, self.scopes)
            flow.user_agent = self.application_name
            credentials = tools.run_flow(flow, store, flags)
            print('Storing credentials to ' + credential_path)

        http = credentials.authorize(httplib2.Http())
        service = discovery.build('gmail', 'v1', http=http)
        return service

    @staticmethod
    def list_unread_emails(service):
        """Retrieves IDs for all unread emails from Google Scholar
        in the inbox.
        :param service: Authorised Gmail Service object
        :return: List of unread email IDs
        """
        try:
            response = service.users().messages()\
                .list(userId='me', q='is:unread from:scholaralerts-noreply@google.com', ).execute()
            p_emails = []
            if 'messages' in response:
                p_emails.extend(response['messages'])
                while 'nextPageToken' in response:
                    page_token = response['nextPageToken']
                    response = service.users().messages().list(userId='me', q='is:unread',
                                                               pageToken=page_token).execute()
                    p_emails.extend(response['messages'])
            return p_emails

        except errors.HttpError as error:
            print(f'An error occurred during unread email retrieval: ${error}')

    @staticmethod
    def get_email_full(service, email_id):
        """
        Get email from inbox via id
        :param service: Authorised Gmail API Service object
        :param email_id: email message GUID
        :return: Email payload
        """
        try:
            p_email = service.users().messages().get(userId='me', id=email_id, format='full').execute()
            return p_email
        except errors.HttpError as error:
            print(f'An error occurred during full-text message retrieval: {error}')

    @staticmethod
    def get_label(g_email):
        """ Loops over labels and extracts custom formats,
        identified as starting with 'Label...'
        :param g_email: Email payload
        :return: Label id string
        """
        label = None

        # Go through labels looking for custom ones
        for lab in g_email['labelIds']:
            match = re.match("Label", lab)
            if match:
                label = lab
                break

        return label

    @staticmethod
    def mark_read(service, unread_email_ids):
        """ Updates processed messages as read.

        :param service: GMail Service object
        :param unread_email_ids: List of email IDs processed during the
        current run.
        :return: None
        """
        # Updates messages to remove 'unread' label
        read_email_ids = [e['id'] for e in unread_email_ids]
        service.users().messages()\
            .batchModify(userId='me', body={'removeLabelIds': ['UNREAD'], 'ids': read_email_ids}).execute()
        return
