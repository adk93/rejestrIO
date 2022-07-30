# Standard library imports
import os
import re
from typing import List
from dataclasses import asdict
import logging

# Third party imports
from dotenv import load_dotenv
import pandas as pd

# Local app imports
from rejestrIO import RejestrIO
from companies_data_reader import read_csv_file
from data_objects import Company, Document

logging.basicConfig(level=logging.INFO)

load_dotenv()

client = RejestrIO(os.environ.get("api_key"))


def get_companies_data(file_path: str) -> List[Company]:
    data = read_csv_file(file_path)

    regex_pattern = r"(?<=\/\/).*?(?=\.pl|\.io|\.com|.eu|\.co|\.it|\.systems|\.healthcare|\.software|\.org|\.pro|\.team|\.agency|\.house|\.biz|\.is|\.global|\.net|\.dev|\.group)"
    companies_data = []

    for company in data:
        logging.info(f"extracting {company}")
        company_name, www = company

        # Extracting everything before Spolka, Sp. z o.o., S.A. etc.
        company_name = re.search(r".*?(?=Sp\.|Spółka|S\.A\.|S\.J\.|,|$)", company_name).group(0)

        krs_number_data = client.get_krs_number_by_name(company_name)

        for entrance in krs_number_data:
            if match := re.search(regex_pattern, www, re.IGNORECASE):
                domain = match.group(0)

                if entrance.www is None:
                    continue

                if domain in entrance.www:
                    companies_data.append(entrance)
        logging.info(f"{company} data extracted")

    pd.DataFrame([asdict(elem) for elem in companies_data]).to_csv(os.path.join("datas", "ALL_COMPANIES.csv"))
    logging.info(f"all companies data saved!")
    return companies_data


def get_documents_list(companies_data: List[Company]) -> List[Document]:

    all_documents = []
    for company in companies_data:
        logging.info(f"extracting documents data for {company}")
        documents = client.get_documents_by_krs_number(company.krs_number)
        all_documents.extend(documents)
        logging.info(f"extracted documents data for {company}")

    pd.DataFrame([asdict(elem) for elem in all_documents]).to_csv(os.path.join("datas", "ALL_DOCUMENTS.csv"))
    logging.info("all documents data saved!")
    return all_documents


def get_documents_content(documents_data: List[Document]) -> pd.DataFrame:

    doc_contents = pd.DataFrame()
    for n, document in enumerate(documents_data):
        logging.info(f"extracing {n} out of {len(documents_data)}")
        content = client.get_document_by_id(document.company_krs, document.document_id)
        df = pd.DataFrame(asdict(content))
        doc_contents = doc_contents.append(df)

        filename = f"{document.company_krs}-{document.document_id}-{document.date_end}-{document.name}.csv"
        file_path = os.path.join("datas", filename)
        df.to_csv(file_path)
    return doc_contents


def main():
    companies_data = get_companies_data("data.csv")
    documents = get_documents_list(companies_data)
    contents = get_documents_content(documents)
    contents.to_csv(os.path.join("datas", "CONTENTS.csv"))


if __name__ == "__main__":
    main()

