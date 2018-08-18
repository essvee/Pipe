from dataclasses import dataclass
from datetime import date

@dataclass
class Citation:
    abstract: str
    author: list
    citation_id: int
    classification: str
    content_version: str
    pipe_created_date: date
    crossref_deposited_date: date
    doi: str
    issue: str
    issued_date: date
    language: str
    # TODO - add Message object as attribute
    # TODO - add Bibliometric object as attribute
    pub_isbn: str
    pub_issn: str
    pub_title: str
    pub_publisher: str
    oa_updated_date: date
    oa_retrieved_date: date
    oa_flag: bool
    oa_best_url: str
    oa_pdf_url: str
    oa_machine_url: str
