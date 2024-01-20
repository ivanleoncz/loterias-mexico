import os
import random

from bs4 import BeautifulSoup
import requests

from utils import detect_lottery_product

# List of UAs to be randomly used, in order to make the request more "legit" on the eyes of the webserver.
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Edg/113.0.14.57",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.3"
]

headers = {
    "User-Agent": random.choice(USER_AGENTS)
}


def download_page(url : str) -> requests:
    """
    Downloads the HTML page which contains the link for the dataset.
    """
    request = requests.get(url, headers=headers, verify=False)
    return request


def get_dataset_url(html_content: str) -> str:
    """
    Obtains URL for downloading dataset, from web page content .
    """
    links = BeautifulSoup(html_content, 'html.parser').find_all('a')
    url = [os.environ["LOTERIA_NACIONAL_URL"] + a["href"].split('..')[-1]  # Transforming URL with double dot notation.
           for a in links if os.environ["BUTTON_TEXT"] in a.get_text()][0]
    return url


def save_dataset(dataset: str) -> None:
    """
    Saves dataset of lottery product.
    """
    with open(detect_lottery_product(dataset), 'w') as f:
        f.write(dataset)


def download_dataset(url, product) -> None:
    """
    Download dataset (.csv) of winning numbers and returns decoded data.

    Parameters
    ----------
    url : provided via argparse, available via .env file
    product : name of the lottery product to be processed
    """
    request = download_page(url)
    dataset_url = get_dataset_url(request.text)
    dataset = requests.get(dataset_url, headers=headers, allow_redirects=True, verify=False)
    save_dataset(dataset.text)
