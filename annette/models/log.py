from sqlalchemy import Column, Date, Integer, Boolean, DateTime
from .base import Base
from .decorators import column_access
from datetime import datetime as dt


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


class RunLogManager(object):
    def __init__(self, session):
        self.log_entry = RunLog()
        self.id = self.log_entry.id
        self.session = session

    def __enter__(self):
        self.log_entry.start = dt.now()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.log_entry.end = dt.now()
        self.session.add(self.log_entry)
        self.session.flush()

    def complete(self, stage):
        setattr(self.log_entry, stage, True)
