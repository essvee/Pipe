from ._utils import logger
from ._base import BaseIdentifier
# import other identifiers here


class IdentifyCore:
    identifiers = []  # list the identifier classes

    @classmethod
    def run(cls):
        # processing code here
        return []

    @classmethod
    def store(cls, session, citations):
        BaseIdentifier.store_citations(citations, session)
        logger.debug(f"{len(citations)} new citations written to citations.")
