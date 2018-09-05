#!/usr/bin/env python

from bs4 import BeautifulSoup
import unicodedata
from pipe.src.message import Message


class MessageFactory(object):
    def __init__(self, source, harvested_date, sent_date, email_body, email_id, label_id=None):
        self.source = source
        self.harvested_date = harvested_date
        self.sent_date = sent_date
        self.email_body = email_body
        self.email_id = email_id
        self.label_id = label_id

    def main(self):
        # Turn body of email into html object
        soup = BeautifulSoup(self.email_body, 'html.parser')

        if self.source == 'GS':
            all_messages = self.parse_gmail(soup)
        else:
            all_messages = None

        return all_messages

    def parse_gmail(self, soup):
        h3 = soup("h3")

        all_messages = []

        for i in h3:
            # Retrieve + parse bib_data
            sibling = i.next_sibling
            bib_data = self.clean_string(sibling.text)
            parsed_bib_data = self.parse_bib_data(bib_data)

            # Get snippet + any bolded text
            snippet = sibling.next_sibling
            snippet_clean = self.clean_string(" ".join(snippet.stripped_strings))

            # Get a list of all bold text
            bold_tag_list = None if snippet.find_all('b') is None else [i.text for i in snippet.find_all('b')]

            # Get distance apart between first and last highlighted term in snippet
            second_bold, first_bold = self.get_indices(bold_tag_list, snippet_clean)
            distance_apart = second_bold - first_bold

            # Check that bold words match scholar alerts
            snippet_match = self.check_context(bold_tag_list)

            # Extract the string around the bold text
            match_context = snippet_clean[first_bold - 10: first_bold + 40] if first_bold >= 0 else None

            # Get title
            title = self.clean_string(i.find('a', class_="gse_alrt_title").text)

            # Build message object + add to list
            all_messages.append(Message(email_id=self.email_id,
                                        harvested_date=self.harvested_date,
                                        sent_date=self.sent_date,
                                        source=self.source,
                                        title=title,
                                        snippet=snippet_clean,
                                        m_author=parsed_bib_data['m_author'],
                                        m_pub_title=parsed_bib_data['m_pub_title'],
                                        m_pub_year=parsed_bib_data['m_pub_year'],
                                        label=self.label_id,
                                        match_context=match_context,
                                        snippet_match=snippet_match
                                        ))

        return all_messages

    def get_indices(self, bold_tag_list, snippet):
        if bold_tag_list is None or isinstance(bold_tag_list, str) or len(bold_tag_list) == 0:
            result = (0, 0)
        else:
            index_positions = [snippet.find(tag) for tag in bold_tag_list]
            result = (max(index_positions), min(index_positions))
        return result

    @staticmethod
    def check_context(bold_tag_list):
        if bold_tag_list is not None:
            # Turn into set to get rid of duplicate tags
            bold_tag_set = [i.lower() for i in bold_tag_list]
            nhm_name = {"natural", "history", "museum", "london"}
            label_patterns = ["nhmuk", "nhml", "bmnh", "bm nh", "nh bm", "10.5519"]
            tag = " ".join(bold_tag_set)

            # return true if highlight matches label, false otherwise
            return bold_tag_set == nhm_name or tag in label_patterns
        else:
            return False

    def parse_bib_data(self, bib_data):
        m_author = None
        m_pub_title = None
        m_pub_year = None

        # Get author name(s)
        parsed_bib = bib_data.split(" - ")
        m_author = self.clean_string(parsed_bib[0])

        # Split further to get year and author - TODO improve this. regex?
        if len(parsed_bib) > 1:
            parsed_b2 = parsed_bib[1].split(',')

            if len(parsed_b2) == 2:
                m_pub_title = self.clean_string(parsed_b2[0])
                m_pub_year = int(self.clean_string(parsed_b2[1]))

            else:
                try:
                    m_pub_year = int(self.clean_string(parsed_b2[0]))
                except ValueError:
                    m_pub_year = None
                    m_pub_title = self.clean_string(parsed_b2[0])

        return {'m_author': m_author, 'm_pub_title': m_pub_title, 'm_pub_year': m_pub_year}

    @staticmethod
    def clean_string(string):
        return unicodedata.normalize("NFKD", string).replace("...", "").strip()
