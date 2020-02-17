from datetime import datetime as dt

from annette.db.models import Access, Citation, ExtractedCitation, Metrics, Name, RunLog, Taxonomy

runlog = RunLog(id=2,
                start=dt.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
                end=dt.strptime('2000-01-01 01:00:00', '%Y-%m-%d %H:%M:%S'),
                harvest=True,
                identify=True,
                enhance=True,
                classify=True)

citation = Citation(doi='10.1002/ajb2.1133',
                    author='Aubriot, Xavier; Knapp, Sandra; Syfert, Mindy M.; Poczai, '
                           'Péter; Buerki, Sven',
                    title='Shedding new light on the origin and spread of the brinjal eggplant ('
                          'Solanum melongena L.) and its wild relatives',
                    type='journal-article',
                    issued_date=dt.strptime('2018-07-01', '%Y-%m-%d'),
                    subject='Plant Science,Genetics,Ecology, Evolution, Behavior and Systematics',
                    pub_title='American Journal of Botany',
                    pub_publisher='Wiley',
                    issn='0002-9122',
                    isbn=None,
                    issue='7',
                    volume='105',
                    page='1175-1187',
                    ecid=1,
                    log_id=2,
                    relevant=True)

extracted_citation = ExtractedCitation(id=1,
                                       email_id='not-a-real-id',
                                       title='Shedding new light on the origin and spread of the '
                                             'brinjal eggplant (Solanum melongena L.) and its '
                                             'wild relatives',
                                       snippet='Page 1. American Journal of Botany 105(7): 1–13, 2018; http://www.wileyonlinelibrary. com/journal/AJB © 2018 Botanical Society of America • 1 Crop wild relatives (CWRs) are likely to play a significant role in securing 21st century',
                                       author='X Aubriot, S Knapp, MM Syfert, P Poczai, S Buerki',
                                       pub_title='American journal of botany',
                                       pub_year=2018,
                                       sent_date=dt.strptime('2018-08-14', '%Y-%m-%d'),
                                       source='GS',
                                       id_status=0,
                                       label_id='Label_4',
                                       doi=None,
                                       snippet_match=0,
                                       highlight_length=0,
                                       last_identify_run=None,
                                       log_id=2
                                       )

metrics = Metrics()

taxonomy = Taxonomy()

access = Access()

name = Name()

classes = {type(i).__name__: i for i in
           [runlog, citation, extracted_citation, metrics, taxonomy, access, name]}
