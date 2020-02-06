from sqlalchemy import Column, Date, Integer, String

from pipe.src.base import Base


class ParsedCitation(Base):
    __tablename__ = 'parsedcitation_store'

    parsedcitation_id = Column(Integer, autoincrement=True, primary_key=True)
    email_id = Column(String)
    title = Column(String)
    snippet = Column(String)
    m_author = Column(String)
    m_pub_title = Column(String)
    m_pub_year = Column(Integer)
    sent_date = Column(Date)
    harvested_date = Column(Date)
    source = Column(String)
    id_status = Column(Integer)
    label_id = Column(String)
    doi = Column(String, default=None)
    last_crossref_run = Column(Date, default=None)
    snippet_match = Column(Integer)
    highlight_length = Column(Integer)

    def get_values(self):
        """
        Returns the object fields
        :return: Tuple
        """
        return (
            self.parsedcitation_id, self.email_id, self.title, self.snippet, self.m_author,
            self.m_pub_title, self.m_pub_year, self.sent_date, self.harvested_date, self.source,
            self.id_status, self.label_id, self.doi, self.last_crossref_run, self.snippet_match,
            self.highlight_length)


class Citation(ParsedCitation):
    pass
