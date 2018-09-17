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
    message_ids: list
    cr_subject: str = None
    cr_pub_title: str = None
    cr_pub_publisher: str = None
    pub_issn: str = None
    pub_isbn: str = None
    cr_issue: str = None
    cr_volume: str = None
    cr_page: str = None
    classification_id: str = None
    nhm_sub: int = 0

    def get_values(self):
        """
        Returns the object fields
        :return: Tuple
        """
        return (self.cr_author, self.cr_doi, self.cr_title, self.cr_type, self.cr_issued_date, self.cr_subject,
                self.cr_pub_title, self.cr_pub_publisher, self.pub_issn, self.pub_isbn, self.cr_issue, self.cr_volume,
                self.cr_page, self.classification_id, self.nhm_sub)