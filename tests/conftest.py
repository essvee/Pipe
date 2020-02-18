import os

import mock
import pytest

from annette.db.session import SessionManager
from . import data

with mock.patch('annette.db.session.SessionManager.database_url',
                os.environ.get('TEST_DATABASE_URL')):
    _sm = SessionManager()


@pytest.fixture(scope='class')
def session_manager():
    _sm.drop()  # ensure we're starting with a clean db
    with _sm:
        for test_data in [data.runlog(), data.extracted_citation(), data.citation()]:
            # run in a loop because some of them depend on each other
            _sm.session.add(test_data)
            _sm.session.flush()
        yield _sm
