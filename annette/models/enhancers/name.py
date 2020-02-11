from sqlalchemy import Column, Integer, String

from ..base import Base
from .. import decorators


@decorators.column_access
@decorators.enhancer('names')
@decorators.logged
class Name(Base):
    label = Column(String)
    usage_key = Column(Integer)
