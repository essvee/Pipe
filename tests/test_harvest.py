import unittest
from datetime import date

import googleapiclient
import pipe.src.gapi


class MyTestCase(unittest.TestCase):

    def test_constructor(self):
        myGapi = pipe.src.gapi.Gapi()
        self.assertTrue(isinstance(myGapi, pipe.src.gapi.Gapi))

    def test_get_credentials(self):
        myGapi = pipe.src.gapi.Gapi()
        result = myGapi.get_credentials()
        self.assertTrue(isinstance(result, googleapiclient.discovery.Resource))
    #
    # def test_get_unread_email_ids(self):
    #     myGapi = pipe.src.gapi.Gapi()
    #     service = myGapi.get_credentials()
    #     unread_emails = myGapi.list_unread_emails(service)
    #     self.assertTrue(unread_emails[0]['id'] == '1654cbffaf5c56a6')

    # def test_get_emails(self):
    #     myGapi = pipe.src.gapi.Gapi()
    #     service = myGapi.get_credentials()
    #     email_id = '1654cbffaf5c56a6'
    #     email = myGapi.get_email(service, email_id)
    #     self.assertTrue(email['id'] == '1654cbffaf5c56a6')

    def test_get_email_creation(self):
        myGapi = pipe.src.gapi.Gapi()
        result = myGapi.main()
        self.assertTrue(result[0].harvested_date == date.today())



if __name__ == '__main__':
    unittest.main()
