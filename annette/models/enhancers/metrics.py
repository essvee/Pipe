from sqlalchemy import Column, Date, Float, Integer

from ..base import Base
from .. import decorators


@decorators.column_access
@decorators.enhancer('bibliometrics')
@decorators.logged
class Metrics(Base):
    times_cited = Column(Integer)
    recent_citations = Column(Integer)
    retrieved_date = Column(Date)
    relative_citation_ratio = Column(Float)
    field_citation_ratio = Column(Float)
