from dataclasses import dataclass
from datetime import date

@dataclass
class Bibliometric:
    retrieved_date: date
    times_cited: int
    recent_citations: int
    relative_citation_ratio: float
    field_citation_ratio: float
