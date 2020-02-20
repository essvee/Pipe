from datetime import datetime as dt, timedelta

import mock
import requests

from annette.db.models import Access
from annette.stages.enhance.unpaywall import UnpaywallEnhancer
from tests.enhance.test_enhancers import TestEnhancer
from .. import data


class TestUnpaywallEnhancer(TestEnhancer):
    enhancer_class = UnpaywallEnhancer
    _date = dt.strptime('2020-01-01T00:00:00.000000', '%Y-%m-%dT%H:%M:%S.%f')

    def test_run_now(self, enhancer, session_manager):
        """
        Tests if enhancer will run/skip when last run in the past 26 weeks.
        """
        assert enhancer.run_now  # with basic test data

        runlog_26weeks = data.runlog(start=dt.now() - timedelta(weeks=26, days=1),
                                     end=dt.now() - timedelta(weeks=26, days=1), enhance=True)
        session_manager.add(runlog_26weeks)
        citation = data.citation(log_id=runlog_26weeks.id, doi='not-a-real-doi')
        session_manager.add(citation)
        access = data.access(log_id=runlog_26weeks.id, doi=citation.doi)
        session_manager.add(access)
        assert enhancer.run_now  # just over 4 weeks ago

        runlog_today = data.runlog(start=dt.now(), end=dt.now(), enhance=True)
        session_manager.add(runlog_today)
        citation.log_id = runlog_today.id
        access.log_id = runlog_today.id
        session_manager.add(citation, access)
        assert not enhancer.run_now  # just now

    def test_handles_error(self, enhancer, mocker):
        error_url = 'http://www.mocky.io/v2/5e4d295e2d00007f00c0daff'  # just a 418 response
        mocker.patch('requests.get', return_value=requests.get(error_url))
        citation = enhancer.get_data()[0]
        assert len(enhancer.get_metadata(citation)) == 0

    def test_returns_access(self, enhancer, mocker):
        response = mock.MagicMock(ok=True)
        response.json.return_value = {
            'best_oa_location': {
                'url': 'http://random-url.xyz',
                'updated': '2020-01-01T00:00:00.000000'
                },
            'is_oa': True,
            'doi': 'test_returns_access-doi'
            }
        mocker.patch('requests.get', return_value=response)
        citation = enhancer.get_data()[0]
        access = enhancer.get_metadata(citation)
        assert len(access) == 1
        assert isinstance(access[0], Access)
        assert access[0].best_oa_url == 'http://random-url.xyz'  # get stats from response
        assert access[0].doi == citation.doi  # get doi from citation, not response

    def test_updates_existing(self, enhancer, mocker, session_manager):
        citation = enhancer.get_data()[0]
        old_access = session_manager.session.query(Access).filter(
            Access.doi == citation.doi).one()

        update_data = {
            'best_oa_location': {
                'host_type': 'testRepository',
                'license': 'test-licence',
                'updated': '2020-01-01T00:00:00.000000',
                'url': 'https://access-test.xyz',
                'url_for_landing_page': 'http://access-test.landing.xyz',
                'url_for_pdf': 'https://access-test.xyz/paper.pdf',
                'version': 'testVersion'
                },
            'data_standard': 2,
            'doi': 'access-test-doi',
            'doi_url': 'https://doi.org/access-test-doi',
            'genre': 'journal-article',
            'has_repository_copy': True,
            'is_oa': True
            }

        # copy it into a dict so it doesn't autoupdate
        old_data = old_access.get_values()

        response = mock.MagicMock(ok=True)
        response.json.return_value = update_data
        mocker.patch('requests.get', return_value=response)

        access = enhancer.get_metadata(citation)
        oa_loc = response.json.return_value['best_oa_location']  # just to make the asserts tidier
        assert len(access) == 1
        assert access[0].id == old_access.id
        assert access[0].doi == citation.doi
        assert old_data != access[0].get_values()
        assert access[0].best_oa_url == oa_loc['url']
        assert access[0].updated_date == self._date
        assert access[0].pdf_url == oa_loc['url_for_pdf']
        assert access[0].is_oa
        assert access[0].host_type == oa_loc['host_type']
        assert access[0].version == oa_loc['version']

    def test_creates_new(self, enhancer, mocker, session_manager):
        runlog = data.runlog(start=dt.now() - timedelta(weeks=5),
                             end=dt.now() - timedelta(weeks=5),
                             enhance=True)
        session_manager.add(runlog)
        citation = data.citation(log_id=runlog.id, doi='test_creates_new_access-doi')
        old_access = session_manager.session.query(Access).filter(
            Access.doi == citation.doi).all()
        assert len(old_access) == 0  # there shouldn't be anything in there with that doi

        response = mock.MagicMock(ok=True)
        response.json.return_value = {
            'best_oa_location': {
                'host_type': 'test-repository',
                'license': 'test-licence',
                'updated': '2020-01-01T00:00:00.000000',
                'url': 'https://access-test.xyz',
                'url_for_landing_page': 'http://access-test.landing.xyz',
                'url_for_pdf': 'https://access-test.xyz/paper.pdf',
                'version': 'testVersion'
                },
            'data_standard': 2,
            'doi': 'access-test-doi',
            'doi_url': 'https://doi.org/access-test-doi',
            'genre': 'journal-article',
            'has_repository_copy': True,
            'is_oa': True
            }
        mocker.patch('requests.get', return_value=response)

        access = enhancer.get_metadata(citation)
        oa_loc = response.json.return_value['best_oa_location']  # just to make the asserts tidier
        assert len(access) == 1
        assert access[0].doi == citation.doi
        assert access[0].best_oa_url == oa_loc['url']
        assert access[0].updated_date == self._date
        assert access[0].pdf_url == oa_loc['url_for_pdf']
        assert access[0].is_oa
        assert access[0].host_type == oa_loc['host_type']
        assert access[0].version == oa_loc['version']
