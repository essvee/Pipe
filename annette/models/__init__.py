from contextlib import contextmanager

from annette.models.base import Base, engine
from .extracted import ExtractedCitation
from .citation import Citation
from .log import RunLogManager
from .enhancers.taxonomy import Taxonomy
from .enhancers.access import Access
from .enhancers.metrics import Metrics
from .enhancers.name import Name


Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    from .base import Session
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
