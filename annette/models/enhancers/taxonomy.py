from sqlalchemy import Column, Integer
from sqlalchemy.dialects import mysql

from .. import decorators
from ..base import Base


@decorators.column_access
@decorators.enhancer
@decorators.logged
class Taxonomy(Base):
    __tablename__ = 'taxonomy'

    id = Column(Integer, autoincrement=True, primary_key=True)
    usageKey = Column(Integer, unique=True)
    scientificName = Column(mysql.TEXT)
    canonicalName = Column(mysql.TEXT)
    rank = Column(mysql.TEXT)
    status = Column(mysql.TEXT)
    kingdom = Column(mysql.TEXT)
    phylum = Column(mysql.TEXT)
    order = Column(mysql.TEXT)
    family = Column(mysql.TEXT)
    species = Column(mysql.TEXT)
    genus = Column(mysql.TEXT)
    kingdomKey = Column(Integer)
    phylumKey = Column(Integer)
    classKey = Column(Integer)
    orderKey = Column(Integer)
    familyKey = Column(Integer)
    genusKey = Column(Integer)
    speciesKey = Column(Integer)
    class_name = Column(mysql.TEXT)
