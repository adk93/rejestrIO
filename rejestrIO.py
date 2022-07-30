# Standard library imports
from typing import List, Tuple, Dict
import json

# Third party imports
import requests

# Local app imports
from data_objects import Company, Document, DocumentContents

REJESTR_IO_RESPONSE = Dict


class RejestrIO:
    """
    Rejestr.io Client

    Makes it easier to extract copmany, document and document conents data

    Args:
        api_key: api_key available in premium account

    Methods:
        get_account_state: retrieves account state
        get_krs_number_by_name: Retrieves a list of objects containing company_name, website and krs based on given name
        get_documents_by_krs_number: Retrieves a list of available documents by a KRS number. Documents as JSON
        get_document_by_id: retrieves an object containing document data as list. Easy to turn into pandas DF

    """
    def __init__(self, api_key: str):
        self.headers = {"Authorization": api_key}

    def _get_request(self, url: str, params: Dict[str, str] | None = None) -> REJESTR_IO_RESPONSE:
        r = requests.get(url, headers=self.headers, params=params)
        return r.json()

    def get_account_state(self) -> REJESTR_IO_RESPONSE:
        url = "https://rejestr.io/api/v2/konto/stan"
        return self._get_request(url)

    def get_krs_number_by_name(self, company_name: str) -> List[Company]:
        url = f"https://rejestr.io/api/v2/org"
        response = self._get_request(url, params={"nazwa": company_name})

        data = []
        for result in response.get("wyniki"):
            name = result.get("nazwy", {}).get("pelna")
            contact = result.get('kontakt', {}).get('www', None)
            krs_number = result.get("numery", {}).get("krs")

            company = Company(name, contact, krs_number)
            data.append(company)

        return data

    def get_documents_by_krs_number(self, krs_number: str) -> List[Document]:
        url = f"https://rejestr.io/api/v2/org/{krs_number}/krs-dokumenty"
        response = self._get_request(url)

        data = []
        for fiscal_year in response:
            date_start = fiscal_year.get("data_start")
            date_end = fiscal_year.get("data_koniec")

            for document in fiscal_year.get("dokumenty", []):
                if document.get("czy_ma_json"):
                    document_id = document.get("id")
                    document_name = document.get("nazwa")

                    doc = Document(krs_number, date_start, date_end, document_name, document_id)
                    data.append(doc)
        return data

    def get_document_by_id(self, krs_number: str, document_id: str) -> DocumentContents:
        url = f"https://rejestr.io/api/v2/org/{krs_number}/krs-dokumenty/{document_id}"
        response = self._get_request(url, params={"format": "json"})

        return DocumentContents(*extract_document_data(response))


def extract_document_data(obj: Dict):
    doc_id = obj.get("id_dokumentu")
    org_id = obj.get("id_organizacji")
    doc_name = obj.get("nazwa")
    date_start = obj.get("okres_data_start")
    date_end = obj.get("okres_data_koniec")

    node_name, label, val = [], [], []

    def contents(content_obj, name=""):
        if type(content_obj) is dict:
            for elem in content_obj:
                contents(content_obj.get(elem), name=elem)

        elif type(content_obj) is list:
            for elem in content_obj:
                contents(elem, name=elem)

        elif name == "nazwa_wezla":
            node_name.append(content_obj)

        elif name == "etykieta":
            label.append(content_obj)

        elif name == "pln_rok_obrotowy_biezacy":
            val.append(content_obj)

    contents(obj.get("zawartosc"))
    doc_ids = [doc_id] * len(node_name)
    org_ids = [org_id] * len(node_name)
    doc_names = [doc_name] * len(node_name)
    date_starts = [date_start] * len(node_name)
    date_ends = [date_end] * len(node_name)

    return doc_ids, org_ids, doc_names, date_starts, date_ends, node_name, label, val
