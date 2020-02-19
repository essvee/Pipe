from datetime import datetime as dt, timedelta

import mock
import requests

from annette.db.models import Metrics
from annette.stages.enhance.dimensions import DimensionsEnhancer
from .test_enhancers import TestEnhancer
from .. import data


class TestDimensionsEnhancer(TestEnhancer):
    enhancer_class = DimensionsEnhancer

    def test_run_now(self, enhancer, session_manager):
        """
        Tests if enhancer will run/skip when last run in the past 4 weeks.
        """
        assert enhancer.run_now  # with basic test data

        runlog_4weeks = data.runlog(start=dt.now() - timedelta(weeks=4, days=1),
                                    end=dt.now() - timedelta(weeks=4, days=1), enhance=True)
        session_manager.add(runlog_4weeks)
        citation = data.citation(log_id=runlog_4weeks.id, doi='not-a-real-doi')
        session_manager.add(citation)
        metrics = data.metrics(log_id=runlog_4weeks.id, doi=citation.doi)
        session_manager.add(metrics)
        assert enhancer.run_now  # just over 4 weeks ago

        runlog_today = data.runlog(start=dt.now(), end=dt.now(), enhance=True)
        session_manager.add(runlog_today)
        citation.log_id = runlog_today.id
        metrics.log_id = runlog_today.id
        session_manager.add(citation, metrics)
        assert not enhancer.run_now  # just now

    def test_handles_error(self, enhancer, mocker):
        error_url = 'http://www.mocky.io/v2/5e4d295e2d00007f00c0daff'  # just a 418 response
        mocker.patch('requests.get', return_value=requests.get(error_url))
        citation = enhancer.get_data()[0]
        assert len(enhancer.get_metadata(citation)) == 0

    def test_returns_metrics(self, enhancer, mocker):
        response = mock.MagicMock(ok=True)
        response.json.return_value = {
            'doi': 'not-a-real-doi',
            'times_cited': 123,
            'recent_citations': 12,
            'highly_cited_1': False,
            'highly_cited_5': False,
            'highly_cited_10': False,
            'relative_citation_ratio': None,
            'field_citation_ratio': None
            }
        mocker.patch('requests.get', return_value=response)
        citation = enhancer.get_data()[0]
        metrics = enhancer.get_metadata(citation)
        assert len(metrics) == 1
        assert isinstance(metrics[0], Metrics)
        assert metrics[0].times_cited == 123  # get stats from response
        assert metrics[0].doi == citation.doi  # get doi from citation, not response

    def test_updates_existing(self, enhancer, mocker, session_manager):
        citation = enhancer.get_data()[0]
        old_metrics = session_manager.session.query(Metrics).filter(
            Metrics.doi == citation.doi).one()

        update_data = {
            'times_cited': 123,
            'recent_citations': 12,
            'relative_citation_ratio': 1.234,
            'field_citation_ratio': 4.321
            }
        old_data = {k: getattr(old_metrics, k) for k in update_data.keys()}
        # make sure the metrics item in the db doesn't match the new values
        # we just want to test if it updates correctly, so just change the value if it's the same
        for k, v in update_data.items():
            if old_data[k] == v:
                update_data[k] = v * 2

        response = mock.MagicMock(ok=True)
        response.json.return_value = update_data
        mocker.patch('requests.get', return_value=response)

        metrics = enhancer.get_metadata(citation)[0]
        assert all([old_data[k] != getattr(metrics, k) for k in update_data.keys()])
        assert all([getattr(metrics, k) == v for k, v in update_data.items()])
        assert metrics.id == old_metrics.id

    def test_creates_new(self, enhancer, mocker, session_manager):
        runlog = data.runlog(start=dt.now()-timedelta(weeks=5), end=dt.now()-timedelta(weeks=5), enhance=True)
        session_manager.add(runlog)
        citation = data.citation(log_id=runlog.id, doi='test_creates_new-doi')
        old_metrics = session_manager.session.query(Metrics).filter(
            Metrics.doi == citation.doi).all()
        assert len(old_metrics) == 0  # there shouldn't be anything in there with that doi

        response = mock.MagicMock(ok=True)
        response.json.return_value = {
            'times_cited': 123,
            'recent_citations': 12,
            'relative_citation_ratio': 1.234,
            'field_citation_ratio': 4.321
            }
        mocker.patch('requests.get', return_value=response)

        metrics = enhancer.get_metadata(citation)
        assert len(metrics) == 1
        assert all([getattr(metrics[0], k) == v for k, v in response.json.return_value.items()])
