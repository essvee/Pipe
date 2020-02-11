from sqlalchemy import Column, Integer, String

from ..base import Base
from .. import decorators


@decorators.column_access
@decorators.enhancer
@decorators.logged
class Taxonomy(Base):
    usageKey = Column(Integer, unique=True)
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
