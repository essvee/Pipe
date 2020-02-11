from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


def column_access(cls):
    cls.columns = classmethod(lambda x: (c.name for c in x.__table__.columns))
    cls.get_values = lambda x: (getattr(x, c) for c in x.columns())
    return cls


def enhancer(tablename):
    from .citation import Citation

    def _enhancer(cls):
        __tablename__ = tablename
        cls.id = Column(Integer, autoincrement=True, primary_key=True)
        cls.doi = Column(ForeignKey(Citation.doi))
        cls.citation = relationship('Citation', backref=tablename)
        return cls

    return _enhancer


def logged(cls):
    from .log import RunLog
    cls.log_id = Column(ForeignKey(RunLog.id))
    cls.log = relationship('RunLog', backref='results')
