from abc import abstractmethod


class BaseIdentifier(object):
    """

    """

    @abstractmethod
    def get_data(self):
        """
        Load the input data.
        :return:
        """
        pass

    @classmethod
    def store_citations(cls, citations, session):
        """
        Store the citations.
        :return:
        """
        session.add_all(citations)
        session.flush()
