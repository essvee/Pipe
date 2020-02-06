import google.auth.credentials
import googleapiclient
import mock
import pytest
from apiclient import errors
from googleapiclient import _auth, discovery, discovery

from annette.harvest import BaseHarvester
from annette.harvest.gmail import GmailHarvester
from annette.models.citation import ParsedCitation
from . import _constants as constants


class TestHarvester:
    harvester_class = BaseHarvester

    @pytest.fixture
    def harvester(self):
        return self.harvester_class()

    @pytest.fixture
    def parse_data_input(self):
        return []

    def test_parse_data_returns_parsed_citations(self, harvester, parse_data_input):
        if getattr(harvester.parse_data, '__isabstractmethod__', False):
            pytest.skip('Unimplemented abstract method.')
        assert isinstance(harvester.parse_data(parse_data_input)[0], ParsedCitation)


class TestGmailHarvester(TestHarvester):
    harvester_class = GmailHarvester

    @pytest.fixture
    def parse_data_input(self):
        return constants.email_list

    @pytest.fixture
    def harvester(self):
        credentials = mock.Mock(spec=google.auth.credentials.Credentials)
        authorized_http = _auth.authorized_http(credentials)
        service = discovery.build('gmail', 'v1', http=authorized_http, cache_discovery=False)
        with mock.patch.object(self.harvester_class, 'get_credentials', return_value=service):
            return self.harvester_class()

    def test_get_credentials(self, harvester):
        assert isinstance(harvester.service, googleapiclient.discovery.Resource)

    def test_list_single_page_emails(self, harvester, mocker):
        email_list = {
            'messages': [{
                'id': '16e08a1e7b38959c',
                'threadId': '16e08a1e7b38959c'
                }, {
                'id': '16e08a1e6d147fa6',
                'threadId': '16e08a1e6d147fa6'
                }, {
                'id': '16e08a1e6c58b1e8',
                'threadId': '16e08a1e6c58b1e8'
                }, {
                'id': '16e08a1e6beb2db8',
                'threadId': '16e08a1e6beb2db8'
                }],
            'resultSizeEstimate': 4
            }
        mocker.patch('googleapiclient.http.HttpRequest.execute',
                     return_value=email_list)
        emails = harvester.list_unread_emails()
        assert len(emails) == 4

    def test_list_multi_page_emails(self, harvester, mocker):
        email_list_1 = {
            'messages': [{
                'id': '16e08a1e7b38959c',
                'threadId': '16e08a1e7b38959c'
                }, {
                'id': '16e08a1e6d147fa6',
                'threadId': '16e08a1e6d147fa6'
                }],
            'nextPageToken': 'abcde',
            'resultSizeEstimate': 4
            }
        email_list_2 = {
            'messages': [{
                'id': '16e08a1e6c58b1e8',
                'threadId': '16e08a1e6c58b1e8'
                }, {
                'id': '16e08a1e6beb2db8',
                'threadId': '16e08a1e6beb2db8'
                }],
            'resultSizeEstimate': 4
            }
        mocker.patch('googleapiclient.http.HttpRequest.execute',
                     side_effect=[email_list_1, email_list_2])
        emails = harvester.list_unread_emails()
        assert len(emails) == 4

    def test_list_no_emails(self, harvester, mocker):
        email_list = {
            'resultSizeEstimate': 0
            }
        mocker.patch('googleapiclient.http.HttpRequest.execute',
                     return_value=email_list)
        emails = harvester.list_unread_emails()
        assert len(emails) == 0

    def test_list_emails_error(self, harvester, mocker):
        error_url = 'https://http.cat/418'
        response = mock.MagicMock(status=418, reason='Is teapot')
        mocker.patch('googleapiclient.http.HttpRequest.execute',
                     side_effect=errors.HttpError(response, b'Is teapot', uri=error_url))
        emails = harvester.list_unread_emails()
        assert emails is None

    def test_get_data(self, harvester, mocker):
        email_id_list = [{
            'id': '16e08a1e7b38959c',
            'threadId': '16e08a1e7b38959c'
            }, {
            'id': '16e08a1e6d147fa6',
            'threadId': '16e08a1e6d147fa6'
            }]
        mocker.patch('annette.harvest.gmail.GmailHarvester.list_unread_emails',
                     return_value=email_id_list)
        mocker.patch('annette.harvest.gmail.ParsedCitationFactory.get_email',
                     side_effect=constants.email_list)
        assert harvester.get_data() == constants.email_list
