import unittest
from datetime import date

from pipe.src.identify_crossref import IdentifyCrossRef
from pipe.src.message import Message

class TestIdentify(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestIdentify, self).__init__(*args, **kwargs)
        self.messages = [Message(message_id=7876,
                                 email_id='165a545c867c3720',
                                 title='Anchonini in Africa: New Species and Genus Confirming'
                                       ' a Transatlantic Distribution (Coleoptera: Curculionidae: Molytinae)',
                                 snippet='Six new species of Anchonini were found during three recent study '
                                       'trips by the African Natural History Research Trust (ANHRT) and '
                                       'The Natural History Museum , London to Mount Nimba in Ivory Coast, '
                                       'the Loma Mountains of Sierra Leone, and São Tomé island',
                                 m_author='J Cristóvão, C Lyal',
                                 m_pub_title='Diversity',
                                 m_pub_year='2018',
                                 sent_date=date.today(),
                                 harvested_date=date.today(),
                                 source='GS',
                                 identification_status=False,
                                 label='Label_8',
                                 snippet_match=True,
                                 highlight_length=25)]
        self.cr = IdentifyCrossRef(self.messages)

    def test_crossref(self):
        identified, unidentified = self.cr.get_crossref_match()
        expected = '10.3390/d10030082'
        self.assertEqual(identified[expected].cr_doi, expected)


if __name__ == '__main__':
    unittest.main()

