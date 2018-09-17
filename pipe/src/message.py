#!/usr/bin/env python
from dataclasses import dataclass
from datetime import date


@dataclass
class Message:
    title: str
    snippet: str
    m_author: str
    m_pub_title: str
    m_pub_year: str
    label: str
    email_id: str
    sent_date: date
    harvested_date: date
    source: str
    snippet_match: bool = False
    identification_status: bool = False
    message_id: int = None
    doi: str = None
    highlight_length: int = None

    def get_values(self):
        """
        Returns the object fields
        :return: Tuple
        """
        return (self.email_id, self.title, self.snippet, self.m_author, self.m_pub_title, self.m_pub_year,
                self.sent_date, self.harvested_date, self.source, self.identification_status, self.label,
                self.doi, self.snippet_match, self.highlight_length)
