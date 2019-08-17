import requests
import urllib
import random
import sys
import json
import importlib
from bs4 import BeautifulSoup
from multiprocessing.dummy import Pool as ThreadPool
from openpyxl import Workbook

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
    for i in range(1, 3):
        url.append('https://bangumi.tv/subject/' + str(i))
    return url

def crawler(url):
    userAgent = random.choice(loadUserAgent('userAgent.txt'))
    print('当前正在爬取 ' + url)
    head = {
            'User-Agent': userAgent,
            'Referer': 'https://bangumi.tv/subject/' + str(random.randint(1, 267658))
        }
    response = requests.get(url, timeout=5, headers=head)
    response.encoding = 'utf-8'
    plain_text = response.text
    soup = BeautifulSoup(plain_text, 'lxml')
    try:
        title = soup.select('.nameSingle > a')[0].get_text()
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
    try:
        number = soup.find_all('span', attrs={'property': 'v:votes'})[0].text
    except:
        number = '暂无'
    try:
        subjectType = soup.select('.nameSingle > small')[0].text
    except:
        subjectType = '暂无'
    
    return [ title, score, infos, number, subjectType ]
    
def print_book_lists_excel(book_lists):
    wb = Workbook()
    ws=wb.active
    ws.append(['序号', '名字', '评分', '投票人数', '类型', '简介'])
    for i, index in book_lists:
        print(i)
        ws.append([index ,i[0], str(i[1]), i[3], i[4], i[2]])
    save_path='book_list'
    save_path+='.xlsx'
    wb.save(save_path)

if __name__ == "__main__":
    pool = ThreadPool(1)
    url = appendUrl()
    
    try:
        results = pool.map(crawler, url)
        print_book_lists_excel(results)
    except Exception as e:
        print(e)
    