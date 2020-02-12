from ._utils import logger
from ._base import BaseEnhancer
from .dimensions import DimensionsEnhancer


class EnhanceCore:
    enhancers = [DimensionsEnhancer]

    @classmethod
    def run(cls, session_manager):
        logger.debug('Beginning enhance stage')
        metadata = []
        for enhancer_type in cls.enhancers:
            logger.debug(f'Running {enhancer_type.__name__}')
            enhancer = enhancer_type()
            citations = enhancer.get_data(session_manager)
            for citation in citations:
                metadata += enhancer.get_metadata(session_manager, citation)
        session_manager.log(metadata)
        logger.debug(f'Finished enhancing. {len(metadata)} new pieces of metadata found.')
        return metadata

    @classmethod
    def store(cls, session_manager, metadata):
        BaseEnhancer.store_metadata(metadata, session_manager)
        logger.debug(f"{len(metadata)} new pieces of metadata stored.")
