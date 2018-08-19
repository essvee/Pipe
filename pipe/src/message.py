class Message(object):
    def __init__(self, title, citation_format, bib_data, snippet, m_author, m_pub_title, m_pub_year):
        self.citation_format = citation_format
        self.title = title
        self.bib_data = bib_data
        self.snippet = snippet
        self.m_author = m_author
        self.m_pub_title = m_pub_title
        self.m_pub_year = m_pub_year

    def extract_bib_data(self):
        # TODO implement this method
        pass
