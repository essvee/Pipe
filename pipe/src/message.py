class Message(object):
    def __init__(self, email_id, citation_format, message_id, bib_data):
        self.email_id = email_id
        self.citation_format = citation_format
        self.message_id = message_id
        self.bib_data = bib_data
        self.m_author = None
        self.m_pub_title = None
        self.m_pub_year = None

    def extract_bib_data(self):
        # TODO implement this method
        pass
