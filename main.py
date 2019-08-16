import requests
import urllib
import random
import sys
import json
import importlib
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool

def loadUserAgent(file):
    uas = []
    with open(file, 'rb') as f:
        for ua in f.readlines():
            if ua:
                uas.append(ua.strip()[:-1])
    random.shuffle(uas)
    return uas

def appendUrl():
    url = []
    for i in range(1, 267658):
        url.append('https://bangumi.tv/subject/' + str(i))
    return url

def crawler(url):
    userAgent = random.choice(loadUserAgent('userAgent.txt'))
    head = {
            'User-Agent': userAgent,
            'Referer': 'https://bangumi.tv/subject/' + str(random.randint(1, 267658))
        }
    response = requests.get(url, headers=head)
    response.encoding = 'utf-8'
    plain_text = response.text
    soup = BeautifulSoup(plain_text, 'lxml')
    try:
        title = soup.find('h1', class_='nameSingle').find('a').string
    except:
        title = '暂无'
    try: 
        score = soup.find('span', class_='number').string
    except:
        score = '暂无'
    try:
        infos = soup.find('div', id='subject_summary').text
    except:
        infos = '暂无'
    
    with open('result.txt', encoding='utf-8',mode='w') as file:
        file.write('名字: ' + title + '评分: ' + score + '简介: ' + infos)
    


if __name__ == "__main__":
    pool = ThreadPool(1)
    url = appendUrl()
    try:
        results = pool.map(crawler, url)
    except Exception as e:
        print(e)
    pool.map(crawler, url)