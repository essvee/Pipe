#!/usr/bin/env python
from dataclasses import dataclass


@dataclass
class Message:
    citation_format: str
    title: str
    bib_data: str
    snippet: str
    m_author: str
    m_pub_title: str
    m_pub_year: str
    label: str
    email_id: str
    message_id: int = None

    def get_message_values_tuple(self):
        return (self.email_id, self.citation_format, self.title,
                self.bib_data, self.snippet, self.m_author,
                self.m_pub_title, self.m_pub_year)
