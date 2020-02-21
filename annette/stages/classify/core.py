from ._utils import logger
from ._base import BaseClassifier


class ClassifyCore:
    classifiers = []

    @classmethod
    def run(cls, session_manager):
        logger.debug('Beginning classify stage')
        citations = BaseClassifier(session_manager).get_data()
        for classifier_type in cls.classifiers:
            classifier = classifier_type(session_manager)
            citations = classifier.process_data(citations)
        session_manager.log(citations)
        logger.debug(f'Finished classifying. {len(citations)} citations processed.')
        return citations

    @classmethod
    def store(cls, session_manager, citations):
        BaseClassifier(session_manager).store_data(citations)
        logger.debug(f'{len(citations)} citations updated.')
