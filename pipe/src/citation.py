#!/usr/bin/env python
from dataclasses import dataclass
from datetime import date


@dataclass
class Citation:
    cr_author: list
    cr_doi: str
    cr_title: str
    cr_type: str
    cr_issued: date
    cr_content_version: str = None
    cr_subject: str = None
    cr_pub_title: str = None
    cr_pub_publisher: str = None
    pub_issn: str = None
    pub_isbn: str = None
    cr_issue: str = None
    cr_volume: str = None
    cr_page: str = None
    cr_url: str = None

