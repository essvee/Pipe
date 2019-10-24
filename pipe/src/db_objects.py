#!/usr/bin/env python
from sqlalchemy import Column, Integer, String, Date, Float, Boolean
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


class Access(Base):
    __tablename__ = 'open_access'

    oa_id = Column(Integer, autoincrement=True, primary_key=True)
    best_oa_url = Column(String)
    updated_date = Column(Date)
    retrieved_date = Column(Date)
    pdf_url = Column(String)
    is_oa = Column(Boolean)
    doi = Column(String)
    doi_url = Column(String)
    host_type = Column(String)
    version = Column(String)

    def get_values(self):
        """
        Returns the object fields
        :return: Tuple
        """
        return (self.oa_id, self.best_oa_url, self.updated_date, self.retrieved_date,
                self.pdf_url, self.is_oa, self.doi, self.doi_url, self.host_type, self.version)


class Name(Base):
    __tablename__ = 'names'

    name_id = Column(Integer, autoincrement=True, primary_key=True)
    doi = Column(String)
    label = Column(String)
    usage_key = Column(Integer)
    rundate = Column(Date)

    def get_values(self):
        """
        Returns the object fields
        :return: Tuple
        """
        return self.name_id, self.doi, self.label, self.rundate


class Taxonomy(Base):
    __tablename__ = 'taxonomy'

    usageKey = Column(Integer, primary_key=True)
    scientificName = Column(String)
    canonicalName = Column(String)
    rank = Column(String)
    status = Column(String)
    kingdom = Column(String)
    phylum = Column(String)
    order = Column(String)
    family = Column(String)
    species = Column(String)
    genus = Column(String)
    kingdomKey = Column(Integer)
    phylumKey = Column(Integer)
    classKey = Column(Integer)
    orderKey = Column(Integer)
    familyKey = Column(Integer)
    genusKey = Column(Integer)
    speciesKey = Column(Integer)
    class_name = Column(String)
    rundate = Column(Date)

    def get_values(self):
        """
        Returns the object fields
        :return: Tuple
        """
        return (self.usageKey, self.scientificName, self.canonicalName, self.rank,
                self.status, self.kingdom, self.phylum, self.order, self.family,
                self.species, self.genus, self.kingdomKey, self.phylumKey, self.classKey,
                self.orderKey, self.familyKey, self.genusKey, self.speciesKey, self.class_name, self.rundate)
