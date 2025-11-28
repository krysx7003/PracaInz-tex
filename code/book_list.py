import json
import os

import requests
from utils.path import is_valid


def get_book_list(use_cache: bool) -> None | list[Book]:
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{AUTHOR}.json")
    if is_valid(path) and use_cache:
        print(f"File {AUTHOR}.json already exists, skipping url call")
        return open_json(path)

    try:
        print(f"Getting: {url}")
        response = requests.get(url, timeout=TIMEOUT_MAX)

        if response.status_code != 200:
            print("Error: ", response.status_code)
            return None

        books_data = response.json()
        if use_cache:
            print(f"Sqving file {AUTHOR}.json")

            data = response.json()
            with open(path, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=2, ensure_ascii=False)

        return [Book(**book) for book in books_data]

    except requests.exceptions.RequestException as e:
        print("Error: ", e)
        return None
