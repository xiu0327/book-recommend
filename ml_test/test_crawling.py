import requests
from bs4 import BeautifulSoup
import json

result={
    'book_list':[]
}

url = 'https://library.busan.go.kr/elib/module/elib/book/view.do?menu_idx=2&book_idx=9283&viewPage=1&search_text=%EC%95%84%EA%B0%80%EB%AF%B8&search_type=&type=ADO&author_name=&book_pubname=&book_year=&rowCount=10&from_search=Y'
response = requests.get(url)
if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    textArr = soup.select('#book > div > div > div.sinfo > div.info')
    title = "아가미"
    #print(textArr[0].select_one('li').text)
    state = textArr[0].select('li')[5].text.split(':')[1].find("가능")
    if state > 0: #대출 가능하다면
        result['book_list'].append(title)
    print(json.dumps(result, ensure_ascii=False, indent='\t'))


else : 
    print(response.status_code)