import google.auth.credentials
import mock
import pytest
from googleapiclient import _auth, discovery

from pipe.harvest.gmail import ParsedCitationFactory
from . import _constants as constants


class TestParsedCitationFactory:
    @pytest.fixture
    def factory(self):
        credentials = mock.Mock(spec=google.auth.credentials.Credentials)
        authorized_http = _auth.authorized_http(credentials)
        service = discovery.build('gmail', 'v1', http=authorized_http, cache_discovery=False)
        return ParsedCitationFactory(service)

    def test_parse_gmail_length(self, factory):
        parsed_citations = factory.parse_email(constants.email_list[0])
        assert len(parsed_citations) == 1
