#!/usr/bin/env python
from dataclasses import dataclass
from datetime import date
from pipe.src.message import Message


@dataclass
class Citation:
    cr_author: list
    cr_doi: str
    harvested_date: date
    cr_issued_date: date
    message: Message
    cr_title: str
    cr_type: str
    cr_content_version: str = None
    cr_subject: str = None
    # TODO - add Bibliometric object as attribute
    cr_pub_title: str = None
    cr_pub_publisher: str = None
    oa_updated_date: date = None
    oa_retrieved_date: date = None
    oa_flag: bool = 0
    oa_best_url: str = None
    oa_pdf_url: str = None
    oa_machine_url: str = None
    pub_issn: str = None
    pub_isbn: str = None
    citation_id: int = None
    classification: str = None
    cr_issue: str = None
    cr_volume: str = None
    cr_page: str = None
