from soynlp.noun import LRNounExtractor_v2
from konlpy.tag import Okt
from krwordrank.word import KRWordRank
from urllib import response
from regex import P
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import NoSuchElementException
import re

def get_data(ID):
    url = "https://m.blog.naver.com/{}?categoryNo=0&listStyle=photo".format(ID)
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    driver = webdriver.Chrome("/home/ubuntu/code/chromedriver", options=options)
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

    links = []
    for i in range(10):
        try:
            target = driver.find_element(By.XPATH, '//*[@id="postlist_block"]/div[2]/div/div[2]/ul/li[{}]/a'.format(i+1)).get_attribute('href')
            links.append(target)
        except NoSuchElementException:
            break

    innerTexts = []

    for link in links:
        response = requests.get(link)
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        removeText = soup.select_one("#ct > div._postView").find('div', 'se-component-content').text
        innerText = soup.select_one("#ct > div._postView").text.replace(removeText, '')
        innerText = re.sub('[ ]+', ' ', re.sub('[^ 가-힣]+',' ', innerText))
        innerTexts.append(innerText[:len(innerText)-70])

    return innerTexts

def get_wordrank_keywords(texts, beta=0.85, max_iter=10):
    from krwordrank.word import KRWordRank
    wordrank_extractor = KRWordRank(
        min_count = 3, # 단어의 최소 출현 빈도수 (그래프 생성 시)
        max_length = 10, # 단어의 최대 길이
        verbose = True
    )
    keywords, rank, graph = wordrank_extractor.extract(texts, beta, max_iter, num_keywords=30)
    return keywords, rank, graph

def prune_keywords(keywords, stopwords, num = 10):
    keyword_list = {}
    if len(keywords) == 0:
        return []
    else:
        for keyword in keywords.keys():
            if keyword not in stopwords:
                keyword_list[keyword] = keywords[keyword]
            if len(keyword_list) > num:
                break
    return keyword_list

def keywords(userid):
    # tokenizer
    okt = Okt()

    texts = get_data(userid)
    noun_extractor = LRNounExtractor_v2(verbose=True)
    soy_nouns = noun_extractor.train_extract([' '.join(texts)])
    tmp = sorted(soy_nouns.items(), key = lambda item: item[1].frequency, reverse = True)
    tmp = [i for i in soy_nouns.items() if i[1].frequency >4]
    tmp = sorted(tmp, key = lambda item: len(item[0]), reverse = True)
    nouns = [i[0] for i in tmp if i[1].frequency>3 and len(i[0])>2][:30]
    okt_nouns = [' '.join(okt.nouns(text)) for text in texts]

    #키워드 추출

    keyword_dict = dict()
    keywords, rank, graph = get_wordrank_keywords(okt_nouns)
    stopwords = ['파일', '첨부', '댓글', '다운로', '다음', '테리', '이장', '유사', '추가', '두께감', '미안', '버스', '케이스', '별로', '정도', '구매', '좋아', '그렇게', '마지막', '최대한', '다음날', '이렇게', '전체적', '이런', '주간', '하이퍼링크', '그럼', '파우', '누군가', '오늘', '만들어', '얘기', '진짜', '오랜만', '이웃추', '분들', '때문', '자신', '김겨', '필요', '억울', '당연', '단계', '베스트', '얼굴', '시리즈', '사용', '제품', '월간', '가격', '스스로', '너무', '요즘', '다음', '사용', '공유','추천', '종이질감필름', '다이소']
    keywords = prune_keywords(keywords, stopwords)
    result = list(set([n for n in nouns if n not in stopwords]))
    result.extend(list((keywords.keys())))
    return {"keywords":result}
