from annette.db.models import Access, Metrics
from annette.stages.enhance import EnhanceCore
from .. import data


class TestCore:
    def test_gets_metadata(self, session_manager, mocker):
        mocker.patch('annette.stages.enhance.dimensions.DimensionsEnhancer.get_metadata',
                     return_value=[data.metrics()])
        mocker.patch('annette.stages.enhance.unpaywall.UnpaywallEnhancer.get_metadata',
                     return_value=[data.access()])
        metadata = EnhanceCore.run(session_manager)
        assert len(metadata) == 2
        assert any([isinstance(m, Metrics) for m in metadata])
        assert any([isinstance(m, Access) for m in metadata])

    def test_skips_recent(self, session_manager, mocker):
        # mock the get_metadata methods just in case
        mocker.patch('annette.stages.enhance.dimensions.DimensionsEnhancer.get_metadata',
                     return_value=['dimensions'])
        mocker.patch('annette.stages.enhance.unpaywall.UnpaywallEnhancer.get_metadata',
                     return_value=['unpaywall'])
        mocker.patch('annette.stages.enhance.dimensions.DimensionsEnhancer.run_now', False)
        mocker.patch('annette.stages.enhance.unpaywall.UnpaywallEnhancer.run_now', False)
        metadata = EnhanceCore.run(session_manager)
        assert len(metadata) == 0

    def test_stores_metadata(self, session_manager):
        metadata = [data.metrics(times_cited=123456789), data.access(best_oa_url='http://test-core-oa-url.com')]
        EnhanceCore.store(session_manager, metadata)
        metrics = session_manager.session.query(Metrics).filter(Metrics.id == metadata[0].id).all()
        access = session_manager.session.query(Access).filter(Access.id == metadata[1].id).all()
        assert len(metrics) > 0
        assert len(access) > 0
        assert metrics[0].times_cited == 123456789
        assert access[0].best_oa_url == 'http://test-core-oa-url.com'
