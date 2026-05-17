import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


PAGE_URL = "https://wiki.cs.money/ru/weapons/ak-47"
FOLDER_NAME = "ak47_skins"


def clean_filename(name):
    name = name.strip()
    name = re.sub(r'[\\/*?:"<>|]', "", name)
    name = name.replace(" ", "_")
    return name[:100]


def download_image(image_url, file_path):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(image_url, headers=headers, timeout=30)
    response.raise_for_status()

    with open(file_path, "wb") as file:
        file.write(response.content)


def main():
    os.makedirs(FOLDER_NAME, exist_ok=True)

    headers = {
        "User-Agent": "Maxim"
    }

    response = requests.get(PAGE_URL, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    weapon_slug = urlparse(PAGE_URL).path.strip("/").split("/")[-1]

    downloaded = 0
    used_urls = set()

    links = soup.find_all("a", href=True)

    for link in links:
        href = link["href"]

        if f"/weapons/{weapon_slug}/" not in href:
            continue

        img = link.find("img")

        if img is None:
            continue

        image_url = img.get("src")

        if not image_url:
            continue

        image_url = urljoin(PAGE_URL, image_url)

        if image_url in used_urls:
            continue

        used_urls.add(image_url)

        alt = img.get("alt", f"skin_{downloaded + 1}")
        file_name = clean_filename(alt) + ".png"
        file_path = os.path.join(FOLDER_NAME, file_name)

        try:
            download_image(image_url, file_path)
            downloaded += 1
            print(f"Downloaded: {file_name}")
        except Exception as error:
            print(f"Error downloading {image_url}: {error}")

    print(f"\nDone. Downloaded images: {downloaded}")


if __name__ == "__main__":
    main()