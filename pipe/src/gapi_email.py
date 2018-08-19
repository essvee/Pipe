from bs4 import BeautifulSoup
import unicodedata

from pipe.src.message import Message


class GapiEmail(object):
    def __init__(self, harvested_date, sent_date, email_body, email_id, label=None):
        self.harvested_date = harvested_date
        self.sent_date = sent_date
        self.email_body = email_body
        self.email_id = email_id
        self.label = label
        self.messages = self.extract_messages()

    def extract_messages(self):
        # Turn body of email into html object
        soup = BeautifulSoup(self.email_body, 'html.parser')
        h3 = soup("h3")

        all_messages = []

        for i in h3:

            # Gets PDF/HTML indicator, if present
            if i.span:
                citation_format = i.span.text
            else:
                citation_format = 'UNKNOWN'


            # Gets bib_data
            sibling = i.next_sibling
            bib_data = self.clean_string(sibling.text)

            # Split on hyphen to get author
            parsed_bib = bib_data.split(' - ')
            m_author = self.clean_string(parsed_bib[0])

            m_pub_title = None
            m_pub_year = None

            # Split further to get year and author - TODO improve this. regex?
            if parsed_bib[1]:
                parsed_b2 = parsed_bib[1].split(',')

                if len(parsed_b2) == 2:
                    m_pub_title = self.clean_string(parsed_b2[0])
                    m_pub_year = self.clean_string(parsed_b2[1])

                else:
                    try:
                        int(parsed_b2[0])
                        m_pub_year = self.clean_string(parsed_b2[0])
                    except ValueError:
                        m_pub_title = self.clean_string(parsed_b2[0])

            # Gets snippet
            snippet = sibling.next_sibling
            snippet_clean = self.clean_string(" ".join(snippet.stripped_strings))

            # Gets title
            title = self.clean_string(i.find('a', class_="gse_alrt_title").text)

            # Build message object
            my_message = Message(citation_format, title, bib_data, snippet_clean, m_author, m_pub_title, m_pub_year)
            all_messages.append(my_message)


        return all_messages

    def clean_string(self, string):
        return unicodedata.normalize("NFKD", string).replace("...", "").strip()
