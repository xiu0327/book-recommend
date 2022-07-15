import requests
from bs4 import BeautifulSoup
from datetime import date, timedelta
import rsa
import time
import codecs
import json

def encrypt(s):
    n = 'B14C5FC5C617CD22650ABF6B3D704D047BE4E86A3786EB7BA1EF23B5CAAE77D70501697204465018B2DDCFBE5C9B590011EAE4F6F5D36EEC01774694EA334C9F295547E80510901316C87C884E75B5F17FB741876CFE49E0E4A155304E242A5FABD109E9C283F67CF75861D2C02093A34145150EA59951BC7D888122713C2CB1'
    e = '10001'
    n, e = int(n, 16), int(e, 16)
    pubkey = rsa.PublicKey(n, e)

    now = round(time.time() * 1000)
    message = (s + ' ' + str(now)).encode()
    encrypted = rsa.encrypt(message, pubkey)
    encrypted64 = codecs.encode(encrypted, 'base64').decode()

    return encrypted64


def get_data(uid, upw):
    url = 'https://library.busan.go.kr/portal/intro/login/loginProc.do'

    header = {
        'Referer': 'https://library.busan.go.kr/portal/intro/login/index.do?menu_idx=44',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:101.0) Gecko/20100101 Firefox/101.0'
    }

    data = {
        'before_url': "/portal/index.do",
        'member_pw': encrypt(upw),
        'member_id': encrypt(uid),
        'target': ''
    }

    session = requests.session()
    session.post(url, headers=header, data=data)

    response = session.get("https://library.busan.go.kr/portal/intro/search/loan/history.do?menu_idx=58")

    start = (date.today() - timedelta(days=365)).isoformat()
    end = date.today().isoformat()
    col = ['bookname', 'lib', 'class_no']

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        page_num = len(soup.select('#board_paging > span > a'))
        book_list = {'books': []}

        for page in range(1, page_num + 1):
            url = f'https://library.busan.go.kr/portal/intro/search/loan/history.do?viewPage={page}&menu_idx=58&search_start_date={start}&search_end_date={end}'
            response = session.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                books = soup.select('div.book-list > table > tbody > tr')
                # books = [[e.string for e in b.select('td')[:3]] for b in books]
                books = [dict(zip(col, [e.string for e in b.select('td')[:3]])) for b in books]
                book_list['books']+=books

            else:
                return 'loan/history table load error' + response.status_code

            if not book_list: return 'login error'

        if book_list:
            return book_list
        else:
            return 'loan/history page load error' + response.status_code
