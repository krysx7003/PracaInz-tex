import os


def scrape(epub_url: str, name: str):
    print("Downloading url: ", epub_url)
    try:
        print(f"Getting: {epub_url}")
        response = requests.get(epub_url, timeout=TIMEOUT_MAX)

        if response.status_code != 200:
            print("Error: ", response.status_code)

        path = os.path.join(RAW_DIR, f"{name}.epub")

        total_size = int(response.headers.get("content-length", 0))
        print(f"Downloading {total_size} bytes...")

        with open(path, "wb") as file:
            if total_size == 0:
                file.write(response.content)
            else:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        downloaded += len(chunk)
                        if total_size > 0:
                            progress = (downloaded / total_size) * 100
                            print(f"Progress: {progress:.1f}%", end="\r")

        print(f"\nSuccessfully saved: {path}")

    except requests.exceptions.RequestException as e:
        print("Error: ", e)
