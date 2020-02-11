from sqlalchemy import Column, Date, Integer, String

from .base import Base
from . import decorators


@decorators.column_access
@decorators.logged
class ExtractedCitation(Base):
    __tablename__ = 'extractedcitations'

    id = Column(Integer, autoincrement=True, primary_key=True)
    email_id = Column(String)
    title = Column(String)
    snippet = Column(String)
    author = Column(String)
    pub_title = Column(String)
    pub_year = Column(Integer)
    sent_date = Column(Date)
    source = Column(String)
    id_status = Column(Integer)
    label_id = Column(String)
    doi = Column(String, default=None)
    snippet_match = Column(Integer)
    highlight_length = Column(Integer)
    last_identify_run = Column(Date, default=None)
