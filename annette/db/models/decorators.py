from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


def column_access(cls):
    cls.columns = classmethod(lambda x: (c.name for c in x.__table__.columns))
    cls.get_values = lambda x: {c: getattr(x, c) for c in x.columns()}
    return cls


def enhancer(cls):
    from .citation import Citation
    cls.doi = Column(ForeignKey(Citation.doi))
    cls.citation = relationship('Citation', backref=cls.__tablename__)
    return cls


def logged(cls):
    from .log import RunLog
    cls.log_id = Column(ForeignKey(RunLog.id))
    cls.log = relationship('RunLog', backref=cls.__tablename__ + '_entries')
    return cls
