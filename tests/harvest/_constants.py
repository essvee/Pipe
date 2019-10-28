from dataclasses import dataclass


@dataclass
class email:
    minimal_body_template = '''<html><body><div><h3><a 
            href="http://scholar.google.co.uk/scholar_url?url=https://data.nhm.ac.uk" 
            class="gse_alrt_title">{title}</a></h3><div>{authors} - {article_source}</div>
            <div class="gse_alrt_sni">specimens used from: {specimen_sources}</div></body></html>'''
    title = 'Test google scholar alert email'
    authors = 'Dr A, Dr B, Dr C'
    journal_title = 'Exciting Journal'
    year = '2019'
    natural_history_museum = 'The <b>Natural</b> <b>History</b> <b>Museum</b>, <b>London</b>'
    nearly_nhm = 'a Natural History Museum that is not in London'
    not_nhm = 'Naturhistorisk museum'


email_list = [
    {
        'id': 'journal_with_year',
        'harvested_date': '2019-01-01',
        'label': 'Label_8',
        'received_date': '2019-01-01',
        'body': email.minimal_body_template.format(title=email.title, authors=email.authors,
                                                   article_source=', '.join(
                                                       [email.journal_title, email.year]),
                                                   specimen_sources=email.natural_history_museum).encode()
        },
    {
        'id': 'journal_without_year',
        'harvested_date': '2019-01-01',
        'label': 'Label_8',
        'received_date': '2019-01-01',
        'body': email.minimal_body_template.format(title=email.title, authors=email.authors,
                                                   article_source=email.journal_title,
                                                   specimen_sources=email.natural_history_museum).encode()
        }
    ]