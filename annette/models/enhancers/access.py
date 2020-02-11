from sqlalchemy import Boolean, Column, Date, String, Integer
from sqlalchemy.dialects import mysql

from ..base import Base
from .. import decorators


@decorators.column_access
@decorators.enhancer
@decorators.logged
class Access(Base):
    __tablename__ = 'open_access'

    id = Column(Integer, autoincrement=True, primary_key=True)
    best_oa_url = Column(mysql.MEDIUMTEXT)
    updated_date = Column(Date)
    retrieved_date = Column(Date)
    pdf_url = Column(mysql.MEDIUMTEXT)
    is_oa = Column(Boolean)
    host_type = Column(String(25))
    version = Column(String(25))
