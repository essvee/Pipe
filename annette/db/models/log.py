from sqlalchemy import Boolean, Column, DateTime, Integer

from .decorators import column_access
from ..session import Base


@column_access
class RunLog(Base):
    __tablename__ = 'runlog'

    id = Column(Integer, primary_key=True, autoincrement=True)
    start = Column(DateTime, default=None)
    end = Column(DateTime, default=None)
    harvest = Column(Boolean, default=False)
    identify = Column(Boolean, default=False)
    enhance = Column(Boolean, default=False)
    classify = Column(Boolean, default=False)
