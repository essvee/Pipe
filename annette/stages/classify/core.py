from ._base import BaseClassifier
from ._utils import logger
from .forest import RandomForestClassifier


class ClassifyCore:
    classifiers = [RandomForestClassifier]

    @classmethod
    def run(cls, session_manager):
        logger.debug('Beginning classify stage')
        citations = BaseClassifier(session_manager).get_data()
        for classifier_type in cls.classifiers:
            classifier = classifier_type(session_manager)
            citations = classifier.process_data(citations)
        session_manager.log(citations)
        classified_true = len([c for c in citations if c.classification_id == '1'])
        logger.debug(
            f'Finished classifying. {len(citations)} citations processed; {classified_true} '
            f'classified as relevant.')
        return citations

    @classmethod
    def store(cls, session_manager, citations):
        BaseClassifier(session_manager).store_data(citations)
        logger.debug(f'{len(citations)} citations updated.')
