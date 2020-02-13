from abc import abstractmethod


class BaseIdentifier(object):
    """

    """

    def __init__(self, session_manager):
        self.session_manager = session_manager

    @abstractmethod
    def get_data(self):
        """
        Load the input data.
        :return:
        """
        pass

    def store_citations(self, citations):
        """
        Store the citations.
        :return:
        """
        self.session_manager.session.add_all(citations)
        self.session_manager.session.flush()
