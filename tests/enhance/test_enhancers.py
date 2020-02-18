import pytest
from annette.stages.enhance import BaseEnhancer
from annette.db.models import Citation


class TestEnhancer:
    enhancer_class = BaseEnhancer

    @pytest.fixture
    def enhancer(self, session_manager):
        return self.enhancer_class(session_manager)

    def test_get_data_returns_citations(self, enhancer):
        if getattr(enhancer.get_data, '__isabstractmethod__', False):
            pytest.skip('Unimplemented abstract method.')
        assert isinstance(enhancer.get_data()[0], Citation)


