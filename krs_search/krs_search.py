import duckduckgo
from utils import read_csv_file, write_csv_file
from typing import List
import re


def build_query(company_name: str, website: str):
    return f"{company_name} {website} numer KRS"


def get_results_from_duckduckgo(query: str) -> dict:
    return duckduckgo.get_json_results(query)


def extract_results_from_duckduckgo(results: dict) -> List:
    organic_results = results.get("organic_results")

    data = []
    for result in organic_results:
        title = result.get('title')
        snippet = result.get('snippet')
        data.append(title + " " + snippet)

    return data


def extract_krs_number_from_results(data: List) -> str:
    krs_pattern = r"KRS\s+(\d{10})"

    for element in data:
        match = re.search(krs_pattern, element)

        if match:
            krs_number = match.group(1)
            return krs_number


def main():
    data = read_csv_file("data2.csv")

    for n, line in enumerate(data):

        try:
            print(f"Reading line {n}")

            company, website = line
            print(f"{company}, {website}")

            query = build_query(company, website)
            print(f"built query {query}")

            results = get_results_from_duckduckgo(query)

            extracted_results = extract_results_from_duckduckgo(results)

            extracted_krs_number = extract_krs_number_from_results(extracted_results)
            print(f"extracted KRS number is {extracted_krs_number}")

            line.append(extracted_krs_number)

        except Exception as e:
            write_csv_file("data_krs_numbers2.csv", data)

    write_csv_file("data_krs_numbers2.csv", data)


if __name__ == "__main__":
    main()




