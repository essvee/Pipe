from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime as dt


with open('annette/data/auth.txt', 'r') as f:
    PWD, USR, DB = f.read().splitlines()

SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{USR}:{PWD}@{DB}?charset=utf8"

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine, autocommit=True)
Base = declarative_base(engine)


class SessionManager:
    def __init__(self):
        from .models import RunLog
        self.session = None
        self.runlog = RunLog()

    def __enter__(self):
        Base.metadata.create_all(engine)
        self.session = Session()
        self.runlog.start = dt.now()
        self.session.add(self.runlog)
        self.session.flush()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.runlog.end = dt.now()
        if exc_type is not None:
            self.session.rollback()
        self.session.add(self.runlog)
        self.session.flush()
        self.session.close()

    def complete(self, stage):
        setattr(self.runlog, stage, True)

    def log(self, items):
        for i in items:
            i.log_id = self.runlog.id
        return items
