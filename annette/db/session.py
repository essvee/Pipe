from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime as dt
import os

Base = declarative_base()


class SessionManager:
    database_url = os.environ.get('DATABASE_URL')

    def __init__(self):
        from .models import RunLog
        self._engine = create_engine(f'mysql+pymysql://{self.database_url}?charset=utf8')
        self._factory = sessionmaker(bind=self._engine)
        self._scope = scoped_session(self._factory)
        self.session = None
        self.runlog = RunLog()

    def __enter__(self):
        self.create()
        self.session = self._scope()
        self.runlog.start = dt.now()
        try:
            self.session.add(self.runlog)
            self.session.flush()
        except Exception as e:
            print(e)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.runlog.end = dt.now()
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.add(self.runlog)
        self.session.flush()
        self.session.close()
        self._scope.remove()

    def complete(self, stage):
        setattr(self.runlog, stage, True)

    def log(self, items):
        for i in items:
            i.log_id = self.runlog.id
        return items

    def create(self):
        Base.metadata.create_all(self._engine)

    def drop(self):
        from .models import RunLog
        Base.metadata.drop_all(self._engine)
        self.runlog = RunLog()
