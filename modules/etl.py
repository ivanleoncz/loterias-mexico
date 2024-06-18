from datetime import datetime
import random

from bs4 import BeautifulSoup
import requests

from . import TABLE_DRAW, TABLE_SCHEDULE, ID_TRIS, ID_MELATE_RETRO, BUTTON_TEXT


class LotteryETL:

    # List of UAs to be randomly used, in order to make the request more "legit" on the eyes of the webserver.
    user_agents = [
        "Mozilla/10.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0",
        "Mozilla/8.9 (Windows NT 10.0; Win64; x64) AppleWebKit/49.32 (KHTML, like Gecko) Chrome/13.1.2 Edg/10.0.1.7",
        "Mozilla/3.8 (Windows NT 10.0; Win64; x64) AppleWebKit/25.36 (KHTML, like Gecko) Chrome/28.2.0 Safari/537.3"
    ]

    headers = {
        "User-Agent": random.choice(user_agents)
    }

    def __init__(self, db):
        self.db = db

    def get_last_draw(self, product: int) -> tuple:
        """
        Get the last draw of Mexico's Loteria Nacional product.
        """
        return self.db.cur.execute(f"""SELECT number FROM {TABLE_DRAW} 
            WHERE lottery_id = ? ORDER BY number DESC LIMIT 1""", (product, )).fetchone()

    @staticmethod
    def get_dataset_url(html_content: str) -> str:
        """
        Obtains URL for downloading dataset, from web page content.

        Parameters
        ----------
        html_content : html body, previously downloaded via request to lottery service URL
        """
        links = BeautifulSoup(html_content, 'html.parser').find_all('a')
        for a in links:
            if BUTTON_TEXT in a.get_text():
                return a["href"].split('..')[-1]
        return ""

    def update_lottery_database(self, line: list, lottery_id: str) -> None:
        """
        Stores lottery draw on database. How it stores, it depends on the lottery product (lottery_id).

        Parameters
        ----------
        line : lottery draw as list, with numbers and other draw related data.
        lottery_id : used for conditioning the database query
        """
        if lottery_id == ID_TRIS:
            self.db.cur.execute(f"""
                        INSERT INTO {TABLE_DRAW} (lottery_id, number, r1, r2, r3, r4, r5, processed_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                                (line[0], line[1], line[2], line[3],
                                 line[4], line[5], line[6], line[7]))
        else:
            self.db.cur.execute(f"""
                        INSERT INTO {TABLE_DRAW} (lottery_id, number, r1, r2, r3, r4, r5, r6, r7, jackpot, processed_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (int(line[0]), int(line[1]), int(line[2]), int(line[3]),
                                 int(line[4]), int(line[5]), int(line[6]), int(line[7]),
                                 int(line[8]), int(line[9]), line[10]))
        self.db.con.commit()

    def update_lottery_data(self, request, lottery_id, dataset_file) -> None:
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
                if len(line) > 0:
                    line = line.decode("utf-8")
                    f_dataset.write(line + "\n")
                    if not header_processed:
                        header_processed = True
                    else:
                        line = line.split(",")
                        if not last_draw or int(last_draw[0]) < int(line[1]):
                            self.update_lottery_database(line, lottery_id)

    def download(self, lottery_id, lottery_website, lottery_url, lottery_dataset) -> None:
        """
        Performs web-scrapping over Mexico's Loteria Nacional website, downloading draw results
        for a particular lottery product.

        Parameters
        ----------
        lottery_id : ID of the lottery product
        lottery_website : website for the lottery service (could be a mocked URL for testing)
        lottery_url : URL for scrapping the URL of the dataset
        lottery_dataset: filesystem path for storing the dataset
        """
        website = requests.get(url=lottery_url, verify=False, headers=self.headers)
        dataset_url = lottery_website + self.get_dataset_url(website.text)
        dataset_request = requests.get(url=dataset_url, verify=False, headers=self.headers, stream=True,
                                       allow_redirects=True)
        self.update_lottery_data(dataset_request, lottery_id, lottery_dataset)
        dataset_request.close()
