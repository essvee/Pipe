from sqlalchemy import Boolean, Column, Date, String

from ..base import Base
from .. import decorators


@decorators.column_access
@decorators.enhancer('open_access')
@decorators.logged
class Access(Base):
    best_oa_url = Column(String)
    updated_date = Column(Date)
    retrieved_date = Column(Date)
    pdf_url = Column(String)
    is_oa = Column(Boolean)
    host_type = Column(String)
    version = Column(String)
