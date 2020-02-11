from sqlalchemy import Column, Date, ForeignKey, String
from sqlalchemy.orm import relationship

from . import decorators
from .base import Base
from .extracted import ExtractedCitation


@decorators.column_access
@decorators.logged
class Citation(Base):
    __tablename__ = 'citations'

    doi = Column(String, primary_key=True)
    author = Column(String)
    title = Column(String)
    type = Column(String)
    issued_date = Column(Date)
    subject = Column(String)
    pub_title = Column(String)
    pub_publisher = Column(String)
    issn = Column(String)
    isbn = Column(String)
    issue = Column(String)
    volume = Column(String)
    page = Column(String)
    ecid = Column(ForeignKey(ExtractedCitation.id))
    raw = relationship('ExtractedCitation', backref='citation')
