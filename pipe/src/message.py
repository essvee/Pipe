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

    # Returns field values as dict
    def get_message_values_dict(self):
        return {'citation_format': self.citation_format, 'title': self.title, 'bib_data': self.bib_data,
                'snippet': self.snippet, 'm_author': self.m_author, 'm_pub_title': self.m_pub_title,
                'm_pub_year': self.m_pub_year, 'label': self.label, 'gapi_email_id': self.gapi_email_id,
                'email_id': self.email_id, 'message_id': self.message_id}

    def get_message_values_tuple(self):
        return (self.email_id, self.citation_format, self.title, self.bib_data,
                self.snippet, self.m_author, self.m_pub_title, self.m_pub_year)