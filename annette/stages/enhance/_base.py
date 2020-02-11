from abc import abstractmethod


class BaseEnhancer(object):
    """
    Get extra metadata for citations.
    """

    @abstractmethod
    def get_data(self):
        """
        Load the input data.
        :return:
        """
        pass

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
