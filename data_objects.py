# Standard library imports
from dataclasses import dataclass
from typing import Optional

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
    document_id: str
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    name: Optional[str] = None


@dataclass
class DocumentContents:
    document_id: str
    company_krs: str
    doc_name: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    node_name: Optional[str] = None
    label: Optional[str] = None
    val: Optional[str] = None
