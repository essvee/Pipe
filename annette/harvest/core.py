from ._utils import logger
from .gmail import GmailHarvester
from ._base import BaseHarvester


class HarvestCore:
    harvesters = [GmailHarvester]

    @classmethod
    def run(cls):
        logger.debug('Beginning harvest')
        parsed_citations = []
        for harvester_type in cls.harvesters:
            logger.debug(f'Running {harvester_type.__name__}')
            harvester = harvester_type()
            data = harvester.get_data()
            parsed_citations += harvester.parse_data(data)
        logger.debug(f'Finished harvest. {len(parsed_citations)} new citations extracted.')
        return parsed_citations

    @classmethod
    def store(cls, session, parsed_citations):
        BaseHarvester.store_citations(parsed_citations, session)
        logger.debug(f"{len(parsed_citations)} new citations writen to parsedcitation_store.")
