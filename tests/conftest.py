import os

import mock
import pytest

from annette.db.session import SessionManager
from .data import citation, extracted_citation, runlog


@pytest.fixture
def session_manager():
    with mock.patch('annette.db.session.SessionManager.database_url',
                    os.environ.get('TEST_DATABASE_URL')):
        session_manager = SessionManager(True)
        session_manager.drop()  # ensure we're starting with a clean db
        with session_manager:
            for test_data in [runlog, extracted_citation, citation]:
                # run in a loop because some of them depend on each other
                session_manager.session.add(test_data)
                session_manager.session.flush()
            yield session_manager
