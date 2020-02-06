import google.auth.credentials
import mock
import pytest
from googleapiclient import _auth, discovery
from apiclient import errors
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

    def test_get_email_data(self, factory, mocker):
        mocker.patch('googleapiclient.http.HttpRequest.execute',
                     return_value=constants.raw_email_data_1)
        email_data = factory._get_email_data('journal_with_year')
        assert email_data['id'] == 'journal_with_year'
        assert isinstance(email_data, dict)

    def test_get_email_data_error(self, factory, mocker):
        error_url = 'https://http.cat/418'
        response = mock.MagicMock(status=418, reason='Is teapot')
        mocker.patch('googleapiclient.http.HttpRequest.execute',
                     side_effect=errors.HttpError(response, b'Is teapot', uri=error_url))
        with pytest.raises(errors.HttpError) as e:
            factory._get_email_data('journal_with_year')
        assert e.type is errors.HttpError
        assert e.value.content == b'Is teapot'

    def test_get_email_labels(self, factory):
        label = factory._get_email_label({'labelIds': ['Label_1', 'Label_2']})
        assert label == 'Label_1'
        label = factory._get_email_label({'labelIds': ['A', 'B']})
        assert label is None