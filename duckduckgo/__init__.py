import requests


def get_json_results(query: str):
    query_url = query.replace(" ", "+")

    params = {
        "engine": "duckduckgo",
        "q": query_url,
        "kl": "pl-pl",
        "api_key": "81417b5791172f54f55c199e3f1601b8d72d049e3b7ca6b0f15efdbc03b9fe4f"
    }

    r = requests.get("https://serpapi.com/search", params=params)

    return r.json()
