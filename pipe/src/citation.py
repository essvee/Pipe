#!/usr/bin/env python
from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Citation:
    cr_author: str
    cr_doi: str
    cr_title: str
    cr_type: str
    cr_issued_date: date
    cr_subject: str = None
    cr_pub_title: str = None
    cr_pub_publisher: str = None
    pub_issn: str = None
    pub_isbn: str = None
    cr_issue: str = None
    cr_volume: str = None
    cr_page: str = None
