#!/usr/bin/env python


from bs4 import BeautifulSoup
import unicodedata
from pipe.src.db_objects import Message


class MessageFactory(object):
    def __init__(self, source, harvested_date, sent_date, email_body, email_id, label_id=None):
        self.source = source
        self.harvested_date = harvested_date
        self.sent_date = sent_date
        self.email_body = email_body
        self.email_id = email_id
        self.label_id = label_id

    def main(self):
        """
        Controls program logic.
        :return: List of Message objects
        """
        # Turn body of email into html object
        soup = BeautifulSoup(self.email_body, 'html.parser')

        if self.source == 'GS':
            all_messages = self.parse_gmail(soup)
        else:
            all_messages = None

        return all_messages

    def parse_gmail(self, soup):
        """
        Parses email html and extracts bibliographic data
        :param soup: Beautiful soup object representing email html
        :return: List of Message objects
        """
        raw_messages = soup("h3")
        all_messages = []

        for i in raw_messages:
            # Retrieve + parse bib_data
            bib_data = i.next_sibling
            parsed_bib_data = self.parse_bib_data(self.clean_string(bib_data.text))

            # Get snippet + features from highlights
            snippet = bib_data.next_sibling
            snippet_clean, highlight_length, snippet_match = self.parse_snippet(snippet)

            # Get title
            title = self.clean_string(i.find('a', class_="gse_alrt_title").text)
            print(f"Email {self.email_id}. Parsing '{title}'...")

            # Build message object + add to list
            all_messages.append(Message(email_id=self.email_id,
                                        title=title,
                                        snippet=snippet_clean,
                                        m_author=parsed_bib_data['m_author'],
                                        m_pub_title=parsed_bib_data['m_pub_title'],
                                        m_pub_year=parsed_bib_data['m_pub_year'],
                                        sent_date=self.sent_date,
                                        harvested_date=self.harvested_date,
                                        source=self.source,
                                        id_status=False,
                                        label_id=self.label_id,
                                        doi="",
                                        snippet_match=snippet_match,
                                        highlight_length=highlight_length
                                        ))

        return all_messages

    def parse_snippet(self, snippet):
        """
        Parses bibliographic data from string
        :param snippet: Snippet preview extracted from email
        :return: tuple containing clean snippet, measure of highlight_distance and boolean
        showing whether the exact query term was found in the snippet.
        """
        snippet_clean = self.clean_string(" ".join(snippet.stripped_strings))
        bold_words = snippet.find_all('b')

        # Return if there's no snippet with highlight
        if bold_words is None:
            return snippet_clean, None, None

        str_snippet = str(snippet)

        # Get a list of all bold text. Turn into str including tags so we're not measuring duplicates
        bold_words_text = [i.text for i in bold_words]
        bold_words_html = [str(i) for i in bold_words]

        # Get distance apart between first and last highlighted term in snippet
        last_bold, first_bold = self.get_indices(bold_words_html, str_snippet)
        highlight_length = last_bold - first_bold

        # Check that bold words match scholar alerts
        snippet_match = self.check_context(bold_words_text)

        return snippet_clean, highlight_length, snippet_match

    @staticmethod
    def get_indices(bold_tag_list, str_snippet):
        """
        Returns the position of the first and last highlights found in the snippet.
        :param bold_tag_list: list of highlighted terms found in the snippet
        :param str_snippet: string version of email preview snippet
        :return: Index of first bold text and index of last bold text found in snippet
        """
        if isinstance(bold_tag_list, str) or len(bold_tag_list) == 0:
            result = (0, 0)
        else:
            index_positions = [str_snippet.find(tag) for tag in bold_tag_list]
            result = (max(index_positions), min(index_positions))
        return result

    @staticmethod
    def check_context(bold_tag_list):
        """
        Checks if the full query term is found in the snippet
        :param bold_tag_list: query terms extracted from the snippet
        :return: True if found, false otherwise
        """
        if bold_tag_list is not None:
            # Turn into set to get rid of duplicate tags
            bold_tag_set = set([i.lower() for i in bold_tag_list])
            nhm_name = {"natural", "history", "museum", "london"}
            label_patterns = ["nhmuk", "nhml", "bmnh", "bm nh", "nh bm", "10.5519"]
            tag = " ".join(bold_tag_set)

            # return true if highlight matches label, false otherwise
            return bold_tag_set == nhm_name or tag in label_patterns
        else:
            return False

    def parse_bib_data(self, bib_data):
        """
        Parses the string containg author name, publication title and pub year.
        :param bib_data: String
        :return: Dict containing author name, publication title and year
        """
        m_author = None
        m_pub_title = None
        m_pub_year = None

        # Get author name(s)
        parsed_bib = bib_data.split(" - ")
        m_author = self.clean_string(parsed_bib[0])

        # Split further to get year and author
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
        """
        Cleans string
        :param string: String to be cleaned
        :return: Clean string
        """
        return unicodedata.normalize("NFKD", string).replace("...", "").strip()
