import pytest
from annette.stages.enhance import BaseEnhancer
from annette.db.models import Citation
from .. import data
from datetime import datetime as dt


class TestEnhancer:
    enhancer_class = BaseEnhancer

    @pytest.fixture
    def enhancer(self, session_manager):
        return self.enhancer_class(session_manager)

    def test_get_data_returns_citations(self, enhancer):
        if getattr(enhancer.get_data, '__isabstractmethod__', False):
            pytest.skip('Unimplemented abstract method.')
        assert isinstance(enhancer.get_data()[0], Citation)

    def test_run_now(self, enhancer, session_manager):
        """
        If not overridden, run_now should return True.
        """
        assert enhancer.run_now
        runlog = data.runlog(start=dt.now(), end=dt.now(), enhance=True)
        session_manager.add(runlog)
        citation = data.citation(log_id=runlog.id, doi='not-a-real-doi')
        session_manager.add(citation)
        assert enhancer.run_now
