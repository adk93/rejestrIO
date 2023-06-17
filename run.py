# Standard library imports
import os
import re
from typing import List, Callable
import logging
import argparse

# Third party imports
from dotenv import load_dotenv

# Local app imports
from rejestrIO_client import RejestrIO
from utils import read_csv_file
from data_objects import Company, Document, DocumentContents
from bigquery_client import get_list_documents, get_list_companies, save_to_bq_dataset, get_list_contents

logging.basicConfig(level=logging.INFO)

load_dotenv()

rejestrio_client = RejestrIO(os.environ.get("api_key"))

companies_db = get_list_companies()
documents_db = get_list_documents()
contents_db = get_list_contents()



def is_document_in_db(document_id: str):
    return document_id in map(lambda x: x.document_id, documents_db)


def is_content_in_db(document_id: str):
    return document_id in map(lambda x: x.doc_id, contents_db)


def parse_documents_by_company(companies_in_db: List[Company]) -> List[Document]:
    """
    Function looks for documents filled in KRS by a KRS Number
    :param companies_in_db:
    :return:
    """
    parsed_documents = []
    for company in companies_in_db:
        logging.info(f"extracting documents data for {company}")
        documents = rejestrio_client.get_documents_by_krs_number(company.krs_number)

        # Check if document already exists
        for document in documents:
            if not is_document_in_db(document.document_id):
                logging.info(f"adding {document} to a list")
                parsed_documents.append(document)

            logging.info(f"{document} already in a database")

        logging.info(f"extracted documents data for {company}")

    logging.info("all documents data saved!")
    return parsed_documents


def parse_content_by_document_id(documents_data: List[Document]) -> List[DocumentContents]:
    """
    Function parses contents of documents given by a list
    :param documents_data:
    :return: List of document contents represented by a dictionary
    """

    parsed_contents = []
    for n, document in enumerate(documents_data):
        logging.info(f"extracing {n} out of {len(documents_data)}")

        if not is_content_in_db(document.document_id):
            logging.info(f"adding {document} info to a list")
            content = rejestrio_client.get_document_by_id(document.company_krs, document.document_id)
            parsed_contents.append(content)

        logging.info(f"{document} data already in a database")

    return parsed_contents


def main(file_path: str, parse_by: str):

    # Get list of all companies
    companies_in_db: List[Company] = get_list_companies()

    # Parse list of documents filled by companies in db
    logging.info("parsing documents...")
    parsed_documents: List[Document] = parse_documents_by_company(companies_in_db)

    logging.info(f"adding {len(parsed_documents)} documents to a database")
    logging.info(f"containing {' | '.join(list(map(lambda x: x.document_id, parsed_documents)))}")

    # Fill BigQuery Table with parsed documents
    logging.info("saving documents to a database")
    save_to_bq_dataset("documents", parsed_documents)

    # Get list of all documents
    documents_in_db: List[Document] = get_list_documents()

    # Parse documents contents based on the documents in db
    logging.info("parsing document contents...")
    parsed_contents: List[DocumentContents] = parse_content_by_document_id(documents_in_db)

    # Fill BigQuery Table with parsed contents
    save_to_bq_dataset("contents", parsed_contents)


if __name__ == "__main__":
    main()

