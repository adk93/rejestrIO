# Standard library imports
from typing import List, Dict
import os
from dataclasses import asdict, dataclass

# Third party imports
from google.cloud import bigquery
from dotenv import load_dotenv

# Local application imports
from data_objects import Company, Document, DocumentContents

load_dotenv()

client = bigquery.Client()

PROJECT_ID = os.environ.get("PROJECT_ID")
DATASET_ID = os.environ.get("DATASET_ID")


def get_list_companies() -> List[Company]:
    """Get list of companies from BigQuery"""

    db_companies = client.query(f"""
    SELECT * FROM {PROJECT_ID}.{DATASET_ID}.companies;
    """).to_dataframe()

    return [Company(company['company_name'],
                    company['www'],
                    company['krs_number']) for n, company in db_companies.iterrows()]


def get_list_documents() -> List[Document]:
    """Get list of all documents from BigQuery"""

    db_documents = client.query(f"""
    SELECT company_krs, document_id FROM {PROJECT_ID}.{DATASET_ID}.documents;
    """).to_dataframe()

    return [Document(company_krs=doc['company_krs'],
                     document_id=doc['document_id']) for n, doc in db_documents.iterrows()]


def get_list_contents() -> List[DocumentContents]:
    """Get list of documents in the table of contents"""

    db_contents = client.query(f"""
    SELECT doc_id, org_id FROM {PROJECT_ID}.{DATASET_ID}.contents;
    """).to_dataframe()

    return [DocumentContents(document_id=content['document_id'],
                             company_krs=content['company_krs']) for n, content in db_contents.iterrows()]


def save_to_bq_dataset(table_name: str, rows_to_insert: List[dataclass] | List[Dict],
                       project_id: str = None, dataset_id: str = None) -> None:
    """
    Function that saves data to a bigquery table
    :param table_name: table name in bigquery as string
    :param rows_to_insert: rows to append to a table. Should be a list of dicts
    :param project_id: project id in BigQuery
    :param dataset_id: dataset id in BigQuery
    :return: None
    """

    project_id = project_id if project_id is not None else PROJECT_ID
    dataset_id = dataset_id if dataset_id is not None else DATASET_ID

    table_id = f"{project_id}.{dataset_id}.{table_name}"

    if isinstance(rows_to_insert[0], dict):
        data = rows_to_insert
    else:
        data = [asdict(row) for row in rows_to_insert]

    table = bigquery.Table.from_string(table_id)
    errors = client.insert_rows_json(table, data)

    if errors:
        print(f"Encountered errors while inserting rows: {errors}")
    else:
        print("New rows added")
