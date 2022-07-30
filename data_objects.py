# Standard library imports
from dataclasses import dataclass, field
from typing import List

# Third party imports

# Local app imports


@dataclass
class Company:
    company_name: str
    www: str
    krs_number: str


@dataclass
class Document:
    company_krs: str
    date_start: str
    date_end: str
    name: str
    document_id: str


@dataclass
class DocumentContents:
    doc_id: List = field()
    org_id: List = field()
    doc_name: List = field()
    date_start: List = field()
    date_end: List = field()
    node_name: List = field()
    label: List = field()
    val: List = field()
