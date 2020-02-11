from annette.models.base import Base, engine
from .extracted import ExtractedCitation
from .citation import Citation
from .base import Session
from .enhancers.taxonomy import Taxonomy
from .enhancers.access import Access
from .enhancers.metrics import Metrics
from .enhancers.name import Name


Base.metadata.create_all(engine)
