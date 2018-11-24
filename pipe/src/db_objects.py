#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, Date

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
    classification_id = Column(Integer)
    nhm_sub = Column(Integer)

    # Need to rethink if this field is necessary/if it can be achieved without a list
    # message_ids: list

    def get_values(self):
        """
        Returns the object fields
        :return: Tuple
        """
        return (self.author, self.doi, self.title, self.type, self.issued_date, self.subject,
                self.pub_title, self.pub_publisher, self.issn, self.isbn, self.issue, self.volume,
                self.page, self.classification_id, self.nhm_sub)


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
    doi = Column(String, nullable=True)
    last_crossref_run = Column(Date, nullable=True)
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

