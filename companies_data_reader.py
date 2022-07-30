# Standard library imports
import csv
from typing import List, Tuple

# Third party imports

# Local app imports


def read_csv_file(file_path: str) -> List[Tuple[str, str]]:
    """Reads csv file to a list of tuples. The CSV file should have company name, and www as columns"""

    with open(file_path) as f:
        csv_reader = csv.reader(f, delimiter=",")
        data = []

        for n, row in enumerate(csv_reader):
            if n == 0:
                continue

            data.append((row[0], row[1]))

        return data
