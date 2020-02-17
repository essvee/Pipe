from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime as dt
import os

Base = declarative_base()


class SessionManager:
    database_url = os.environ.get('DATABASE_URL')

    def __init__(self, testing=False):
        from .models import RunLog
        self._engine = create_engine(f'mysql+pymysql://{self.database_url}?charset=utf8')
        self.session = None
        self.runlog = RunLog()
        self._do_not_log = testing

    def __enter__(self):
        self.create()
        self.session = sessionmaker(bind=self._engine, autocommit=True)()
        self.runlog.start = dt.now()
        self.session.add(self.runlog)
        self.session.flush()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.runlog.end = dt.now()
        if exc_type is not None:
            self.session.rollback()
        if self._do_not_log:
            # there's no point in writing logs from running test suites
            from .models import RunLog
            self.session.query(RunLog).filter(RunLog.id == self.runlog.id).delete()
        else:
            self.session.add(self.runlog)
        self.session.flush()
        self.session.close()

    def complete(self, stage):
        setattr(self.runlog, stage, True)

    def log(self, items):
        for i in items:
            i.log_id = self.runlog.id
        return items

    def create(self):
        Base.metadata.create_all(self._engine)

    def drop(self):
        Base.metadata.drop_all(self._engine)
