import os
import random

from bs4 import BeautifulSoup
import requests


class ETL:

    # List of UAs to be randomly used, in order to make the request more "legit" on the eyes of the webserver.
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/49.32 (KHTML, like Gecko) Chrome/13.0.0.0 Edg/10.0.1.7",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.3"
    ]

    headers = {
        "User-Agent": random.choice(user_agents)
    }

    def __init__(self, db_cursor):
        self.db = db_cursor

    def get_last_draw(self, product: int) -> tuple:
        """
        Get the last draw of Mexico's Loteria Nacional product.
        """
        return self.db.cur.execute("SELECT number FROM draw WHERE lottery_id = ? ",
                                   (product, )).fetchone()

    def download_page(self, url: str) -> requests:
        """
        Downloads the HTML page which contains the link for the dataset.
        """
        request = requests.get(url, headers=self.headers, verify=False)
        return request

    @staticmethod
    def get_dataset_url(html_content: str) -> str:
        """
        Obtains URL for downloading dataset, from web page content.

        Parameters
        ----------
        html_content : html body, previously downloaded via request to lottery service URL
        """
        links = BeautifulSoup(html_content, 'html.parser').find_all('a')
        # Transforming URL with double dot notation.
        url = [os.environ["LOTERIA_NACIONAL_URL"] + a["href"].split('..')[-1]
               for a in links if os.environ["BUTTON_TEXT"] in a.get_text()][0]
        return url

    def update_lottery_database(self, line: list, lottery_id: str) -> None:
        """
        Stores lottery draw on database. How it stores, it depends on the lottery product (lottery_id).

        Parameters
        ----------
        line : lottery draw as list, with numbers and other draw related data.
        lottery_id : used for conditioning the database query
        """
        # TODO: must add draw date on the queries... datetime.strptime(...)
        if lottery_id == os.environ["LOTERIA_NACIONAL_ID_TRIS"]:
            self.db.cur.execute("""
                        INSERT INTO draw (lottery_id, number, r1, r2, r3, r4, r5)
                        VALUES (?, ?, ?, ?, ?, ?, ?)""",
                                (int(line[0]), int(line[1]), int(line[2]), int(line[3]),
                                 int(line[4]), int(line[5]), int(line[6])))
        else:
            self.db.cur.execute("""
                        INSERT INTO draw (lottery_id, number, r1, r2, r3, r4, r5, r6, r7, jackpot)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (int(line[0]), int(line[1]), int(line[2]), int(line[3]),
                                 int(line[4]), int(line[5]), int(line[6]), int(line[7]),
                                 int(line[8])))

    def update_lottery_dataset(self, request, lottery_id, dataset_file) -> None:
        """
        Updates the CSV dataset which contains all draws for a specific lottery product.
        Database will also be updated, if the draw number is greater than the last draw stored.

        Parameters
        ----------
        request : request object, containing the response (dataset of draw results)
        lottery_id : id of the lottery product (searching last database draw available)
        dataset_file : absolute path for saving the updated draw results
        """
        last_draw = self.get_last_draw(lottery_id)
        with open(dataset_file, 'w') as f_dataset:
            header_processed = False
            for line in request.iter_lines():
                line = line.decode("utf-8")
                f_dataset.write(line)
                if not header_processed:
                    header_processed = True
                else:
                    line = line.split(",")
                    if last_draw and int(last_draw[0]) < int(line[1]) or not last_draw:
                        if int(last_draw[0]) == int(line[1]):
                            print("\n-----\n>>> Inserting repeated!\n-----\n")
                        self.update_lottery_database(line, lottery_id)

    def download(self, lottery_id) -> None:
        """
        Performs web-scrapping over Mexico's Loteria Nacional website, downloading draw results
        for a particular lottery product.

        Parameters
        ----------
        lottery_id : ID of the lottery product
        """
        lottery_url = lottery_dataset = None
        if lottery_id == os.environ["LOTERIA_NACIONAL_ID_TRIS"]:
            lottery_url = os.environ["LOTERIA_NACIONAL_URL_TRIS"]
            lottery_dataset = os.environ["DATASET_PATH_TRIS"]
        elif lottery_id == os.environ["LOTERIA_NACIONAL_ID_MELATE_RETRO"]:
            lottery_url=os.environ["LOTERIA_NACIONAL_URL_MELATE_RETRO"]
            lottery_dataset = os.environ["DATASET_PATH_MELATE_RETRO"]

        lottery_page = self.download_page(lottery_url)
        dataset_url = self.get_dataset_url(lottery_page.text)
        # TODO: this could be handle with download_page, but passing parameters
        request = requests.get(dataset_url, stream=True, headers=self.headers, allow_redirects=True, verify=False)
        self.update_lottery_dataset(request, lottery_id, lottery_dataset)
        request.close()