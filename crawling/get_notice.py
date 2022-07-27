import requests
from bs4 import BeautifulSoup


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

        return notice_list, date_list

    else:
        print(response.status_code)
