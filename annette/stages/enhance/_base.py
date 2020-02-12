from abc import abstractmethod
from annette.db.models import Citation


class BaseEnhancer(object):
    """
    Get extra metadata for citations.
    """

    def get_data(self, session_manager):
        """
        Load the input data.
        :return:
        """
        return session_manager.session.query(Citation).filter(Citation.relevant).all()

    @abstractmethod
    def get_metadata(self, citation):
        """
        Get extra metadata about the citation.
        :return: list of enhancer/metadata instances
        """
        pass

    @classmethod
    def store_metadata(cls, metadata, session):
        """
        Store the extracted citation data.
        :return:
        """
        session.add_all(metadata)
        session.flush()
