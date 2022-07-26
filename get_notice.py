import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

tabulate.WIDE_CHARS_MODE = False


def get_notice():
    url = "https://www.gachon.ac.kr/kor/3104/subview.do"

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        notices_table = soup.select('table > tbody > tr > td.td-subject > a > strong')
        date_table = soup.select('table > tbody > tr > td.td-date')

        notice_list = [notice.get_text() for notice in notices_table]
        date_list = [dates.get_text() for dates in date_table]

        notice_dict = {"작성일": date_list, "제목": notice_list}

        df = pd.DataFrame(notice_dict)

        return tabulate(df, headers='keys', tablefmt='simple', showindex=False)

    else:
        print(response.status_code)
