from ._utils import logger
from ._base import BaseEnhancer
from .dimensions import DimensionsEnhancer
from .unpaywall import UnpaywallEnhancer


class EnhanceCore:
    enhancers = [DimensionsEnhancer, UnpaywallEnhancer]

    @classmethod
    def run(cls, session_manager):
        logger.debug('Beginning enhance stage')
        metadata = []
        for enhancer_type in cls.enhancers:
            logger.debug(f'Running {enhancer_type.__name__}')
            enhancer = enhancer_type(session_manager)
            citations = enhancer.get_data()
            for citation in citations:
                metadata += enhancer.get_metadata(citation)
        session_manager.log(metadata)
        logger.debug(f'Finished enhancing. {len(metadata)} new pieces of metadata found.')
        return metadata

    @classmethod
    def store(cls, session_manager, metadata):
        BaseEnhancer(session_manager).store_metadata(metadata)
        logger.debug(f"{len(metadata)} new pieces of metadata stored.")
