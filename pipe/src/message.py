from dataclasses import dataclass


@dataclass
class Message:
    title: str
    citation_format: str
    bib_data: str
    snippet: str
    m_author: str
    m_pub_title: str
    m_pub_year: int
    message_id: int = None

