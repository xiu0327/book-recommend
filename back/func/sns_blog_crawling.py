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
