#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, Date, Float

from pipe.src.base import Base


class Citation(Base):
    __tablename__ = 'citation_store'

    author = Column(String)
    doi = Column(String, primary_key=True)
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
    classification_id = Column(Integer, default=None)
    identified_date = Column(Integer, default=None)

    def get_values(self):
        """
        Returns the object fields
        :return: Tuple
        """
        return (self.author, self.doi, self.title, self.type, self.issued_date, self.subject,
                self.pub_title, self.pub_publisher, self.issn, self.isbn, self.issue, self.volume,
                self.page, self.classification_id, self.identified_date)


class Message(Base):
    __tablename__ = 'message_store'

    message_id = Column(Integer, autoincrement=True, primary_key=True)
    email_id = Column(String)
    title = Column(String)
    snippet = Column(String)
    m_author = Column(String)
    m_pub_title = Column(String)
    m_pub_year = Column(Integer)
    sent_date = Column(Date)
    harvested_date = Column(Date)
    source = Column(String)
    id_status = Column(Integer)
    label_id = Column(String)
    doi = Column(String, default=None)
    last_crossref_run = Column(Date, default=None)
    snippet_match = Column(Integer)
    highlight_length = Column(Integer)

    def get_values(self):
        """
        Returns the object fields
        :return: Tuple
        """
        return (self.message_id, self.email_id, self.title, self.snippet, self.m_author, self.m_pub_title, self.m_pub_year,
                self.sent_date, self.harvested_date, self.source, self.id_status, self.label_id,
                self.doi, self.last_crossref_run, self.snippet_match, self.highlight_length)


class Metric(Base):
    __tablename__ = 'bibliometrics'

    bibliometric_id = Column(Integer, autoincrement=True, primary_key=True)
    times_cited = Column(Integer)
    recent_citations = Column(Integer)
    retrieved_date = Column(Date)
    relative_citation_ratio = Column(Float)
    field_citation_ratio = Column(Float)
    doi = Column(String)

    def get_values(self):
        """
        Returns the object fields
        :return: Tuple
        """
        return (self.bibliometric_id, self.times_cited, self.recent_citations, self.retrieved_date,
                self.relative_citation_ratio, self.field_citation_ratio, self.doi)

