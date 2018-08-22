from datetime import date

from bs4 import BeautifulSoup
import unicodedata
from pipe.src.message import Message


class GapiEmail(object):
    def __init__(self, harvested_date, sent_date, email_body, email_id, label=None):
        self.harvested_date = harvested_date.strftime('%Y-%m-%d')
        self.sent_date = sent_date
        self.email_body = email_body
        self.email_id = email_id
        self.label_id = label
        self.messages = self.extract_messages()
        self.email_count = len(self.messages)

    def extract_messages(self):
        # Turn body of email into html object
        soup = BeautifulSoup(self.email_body, 'html.parser')
        h3 = soup("h3")

        all_messages = []

        for i in h3:
            citation_format = i.span.text if i.span in i else 'UNKNOWN'

            # Retrieve + parse bib_data
            sibling = i.next_sibling
            bib_data = self.clean_string(sibling.text)
            parsed_bib_data = self.parse_bib_data(bib_data)

            # Get snippet
            snippet = sibling.next_sibling
            snippet_clean = self.clean_string(" ".join(snippet.stripped_strings))

            # Get title
            title = self.clean_string(i.find('a', class_="gse_alrt_title").text)

            # Build message object + add to list
            all_messages.append(Message(citation_format=citation_format,
                                        title=title,
                                        bib_data=bib_data,
                                        snippet=snippet_clean,
                                        m_author=parsed_bib_data['m_author'],
                                        m_pub_title=parsed_bib_data['m_pub_title'],
                                        m_pub_year=parsed_bib_data['m_pub_year'],
                                        label=self.label_id,
                                        email_id=self.email_id))

        return all_messages

    def parse_bib_data(self, bib_data):
        m_author = None
        m_pub_title = None
        m_pub_year = None

        # Get author name(s)
        parsed_bib = bib_data.split(' - ')
        m_author = self.clean_string(parsed_bib[0])

        # Split further to get year and author - TODO improve this. regex?
        if len(parsed_bib) > 1:
            parsed_b2 = parsed_bib[1].split(',')

            if len(parsed_b2) == 2:
                m_pub_title = self.clean_string(parsed_b2[0])
                m_pub_year = int(self.clean_string(parsed_b2[1]))

            else:
                try:
                    m_pub_year = self.clean_string(parsed_b2[0])
                except ValueError:
                    m_pub_title = self.clean_string(parsed_b2[0])

        return {'m_author': m_author, 'm_pub_title': m_pub_title, 'm_pub_year': m_pub_year}

    @staticmethod
    def clean_string(string):
        return unicodedata.normalize("NFKD", string).replace("...", "").strip()

    # Returns field values as tuple
    def get_values(self):
        return (self.email_id, self.harvested_date, self.sent_date, self.label_id,
                self.email_count)
