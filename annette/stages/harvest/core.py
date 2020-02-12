from ._utils import logger
from .gmail import GmailHarvester
from ._base import BaseHarvester


class HarvestCore:
    harvesters = [GmailHarvester]

    @classmethod
    def run(cls, session_manager):
        logger.debug('Beginning harvest')
        extracted_citations = []
        for harvester_type in cls.harvesters:
            logger.debug(f'Running {harvester_type.__name__}')
            harvester = harvester_type()
            data = harvester.get_data()
            extracted_citations += harvester.parse_data(data)
        extracted_citations = session_manager.log(extracted_citations)
        logger.debug(f'Finished harvest. {len(extracted_citations)} new citations extracted.')
        return extracted_citations

    @classmethod
    def store(cls, session_manager, extracted_citations):
        BaseHarvester.store_citations(extracted_citations, session_manager.session)
        logger.debug(f"{len(extracted_citations)} new citations written to extractedcitations.")
