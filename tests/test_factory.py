import unittest
from bs4 import BeautifulSoup
import dill as pickle
from pipe.src.message_factory import MessageFactory


class TestFactory(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestFactory, self).__init__(*args, **kwargs)
        self.email_body = self.load_email()
        self.factory = MessageFactory('GS', '2018-09-04', '2018-08-31', self.email_body, '1656fcdd72fb8d4f')
        self.soup = BeautifulSoup(self.email_body, 'html.parser')

    @staticmethod
    def load_email():
        with open('email_body.pk', 'rb') as f:
            email_body = pickle.load(f)
        return email_body

    def test_parse_gmail_length(self):
        messages = self.factory.parse_gmail(self.soup)
        self.assertTrue(len(messages) == 5)

    def test_parse_gmail_pub_year(self):
        messages = self.factory.parse_gmail(self.soup)
        self.assertTrue(messages[0].m_pub_year == 2018)

    def test_parse_gmail_title(self):
        messages = self.factory.parse_gmail(self.soup)
        self.assertTrue(messages[0].title == 'Does postcranial palaeoneurology provide insight into pterosaur '
                                             'behaviour and lifestyle? New data from the azhdarchoid Vectidraco '
                                             'and the ornithocheirids')

    def test_parse_gmail_snippet_match(self):
        messages = self.factory.parse_gmail(self.soup)
        self.assertFalse(messages[4].snippet_match)


if __name__ == '__main__':
    unittest.main()

