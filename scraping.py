import os

from bs4 import BeautifulSoup
import requests


def get_dataset_url(request) -> str:
    """
    Obtains dataset URL from downloaded page.
    """
    links = BeautifulSoup(request.text, 'html.parser').find_all('a')
    url = [os.environ["LOTERIA_NACIONAL"] + a["href"].split('..')[-1] for a in links
           if os.environ["BUTTON_TEXT"] == a.get_text()]  # Transforming URL with double dot notation...
    return url[0]


def download_page_content(url):
    request = requests.get(url, verify=False)
    return request


def detect_lottery(content: str) -> str:
    """
    Detect lottery product and return the filesystem path for the dataset.
    """
    product_number = content.split('\n')[1].split(',')[0]
    if product_number == '60':
        return os.environ["DATASET_PATH_TRIS"]
    elif product_number == '30':
        return os.environ["DATASET_PATH_MELATE_RETRO"]


def save_dataset(dataset : str) -> None:
    """
    Saves dataset of lottery product.
    """
    with open(detect_lottery(dataset), 'w') as f:
        f.write(dataset)


def download_dataset(url) -> None:
    """
    Download dataset (.csv) of winning numbers and returns decoded data.

    Parameters
    ----------
    url : provided via argparse, available via .env file
    """
    request = download_page_content(url)
    dataset_url = get_dataset_url(request)
    dataset = requests.get(dataset_url, allow_redirects=True, verify=False)
    save_dataset(dataset.text)
