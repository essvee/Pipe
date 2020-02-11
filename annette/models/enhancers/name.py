from sqlalchemy import Column, Integer, String

from .. import decorators
from ..base import Base


@decorators.column_access
@decorators.enhancer
@decorators.logged
class Name(Base):
    __tablename__ = 'names'

    id = Column(Integer, autoincrement=True, primary_key=True)
    label = Column(String(100))
    usage_key = Column(Integer)
