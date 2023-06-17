# Standard library imports
import csv
from typing import List

# Third party imports

# Local app imports


def read_csv_file(file_path: str) -> List[List]:
    """Reads csv file to a list of lists."""

    with open(file_path) as f:
        csv_reader = csv.reader(f, delimiter=",")
        data = []

        for n, row in enumerate(csv_reader):

            data.append([*row])

        return data


def write_csv_file(file_path: str, data: List[List]) -> None:
    with open(file_path, "w", newline="") as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerows(data)