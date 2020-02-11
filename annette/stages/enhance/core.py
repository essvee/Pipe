from ._utils import logger
from ._base import BaseEnhancer


class EnhanceCore:
    enhancers = []

    @classmethod
    def run(cls):
        logger.debug('Beginning enhance stage')
        metadata = []
        for enhancer_type in cls.enhancers:
            logger.debug(f'Running {enhancer_type.__name__}')
            enhancer = enhancer_type()
            citations = enhancer.get_data()
            for citation in citations:
                metadata += enhancer.get_metadata(citation)
        logger.debug(f'Finished enhancing. {len(metadata)} new pieces of metadata found.')
        return metadata

    @classmethod
    def store(cls, session, metadata):
        BaseEnhancer.store_metadata(metadata, session)
        logger.debug(f"{len(metadata)} new pieces of metadata stored.")
