import httplib2
import os
from bs4 import BeautifulSoup
from apiclient import discovery, errors
from oauth2client import client, tools
from oauth2client.file import Storage
import base64
import google.auth

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modified, delete previously saved credentials at ~/.credentials/gmail-credentials.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'DCP Pipeline'


def get_credentials():
    """Gets user credentials from storage.
    If credentials not found or invalid, the OAuth2 flow
    is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')

    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-credentials.json')
    store = Storage(credential_path)

    credentials = store.get()

    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:
            # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def main():
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    # Gets list of ids of unread messages
    unread_messages = list_unread_messages(service)

    # for n in unread_messages:
    message = get_message(service, '1646083b5b48bb8d')
    labels = message['labelIds']
    body_decoded = base64.urlsafe_b64decode(message['payload']['body']['data']).decode("utf-8")

    # Turns body of email into html object
    soup = BeautifulSoup(body_decoded, 'html.parser')
    h3 = soup("h3")

    for n in h3:
        # Gets PDF/HTML indicator, if present
        if n.span:
            format = n.span.text

        # Gets author/journal/pub date
        bib_details = n.next_sibling
        bib_details_text = bib_details.text

        # Gets snippet matching search query
        snippet = bib_details.next_sibling
        snippet_text = " ".join(snippet.stripped_strings)

        # Gets title
        title = n.find('a', class_="gse_alrt_title").text


def list_unread_messages(service):
    """Lists all unread Messages of the user's mailbox ,
    :param service: Authorised Gmail API Service object
    :return: List of Message IDs
    """
    try:
        response = service.users().messages().list(userId='me', q='is:unread').execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])
            while 'nextPageToken' in response:
                page_token = response['nextPageToken']
                response = service.users().messages().list(userId='me', q='is:unread', pageToken=page_token).execute()
                messages.extend(response['messages'])

            return messages
    except errors.HttpError as error:
        print(f'An error occurred: ${error}')


def get_message(service, msg_id):
    """
    Get message from inbox via id
    :param service: Authorised Gmail API Service object
    :param msg_id: email message GUID
    :return: Message payload
    """
    try:
        message = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        return message
    except errors.HttpError as error:
        print(f'An error occurred: ${error}')


if __name__ == '__main__':
    main()
