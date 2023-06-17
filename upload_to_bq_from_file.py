# Standard library imports
import os
from typing import List, Dict
import logging

# Third party imports

# Local app imports
from utils import read_csv_file
from bigquery_client import save_to_bq_dataset


def process_file(file: List[List]) -> List[Dict]:
    headers = file[0]

    file_contents = []
    for row in file[1:]:
        row_dict = {}
        for header, column in zip(headers, row):
            if header == '':
                continue
            row_dict[header] = column
        file_contents.append(row_dict)

    return file_contents


def main():
    filepath = os.path.join("datas", "CONTENTS.csv")
    file = read_csv_file(filepath)
    processed_file = process_file(file)
    save_to_bq_dataset("document_contents", processed_file, "tpx-operations", "comps")


if __name__ == "__main__":
    main()
