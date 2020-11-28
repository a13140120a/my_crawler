import requests
from bs4 import BeautifulSoup
import os
import time
import json
import random
from lxml import etree

StartTime = time.time()


os.makedirs('CVSpttArticle',exist_ok=True)

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'
headers = {
    'User-Agent': ua
}
url = 'https://www.ptt.cc/bbs/CVS/index.html'

for page in range(0,1):
    # print(url)
    res = requests.get(url, headers=headers)
    # print(res.text)
    soup = BeautifulSoup(res.text, 'html.parser')
    html = etree.HTML(res.text)
    #title = soup.select('div.title')
    number = html.xpath('//div[@class="title"]/ancestor::div/text()')
    title = html.xpath('//div[@class="title"]/a/text()')
    print(number)  #在這裡~~!!
    print(len(title))
    print(title)
    for t in title:
        try:
            title_name = t.findAll('a')[0].text
            # print(title_name)
            tmp_a_tag = t.findAll('a')
            # print(tmp_a_tag)
            title_url = 'https://www.ptt.cc' + t.findAll('a')[0]['href']
            res = requests.get(title_url, headers=headers)
            # print(title_name, title_url)

            # Get article by title_url
            res_article = requests.get(title_url, headers=headers)
            soup_article = BeautifulSoup(res_article.text, 'html.parser')
            all_content = soup_article.select('div [id="main-content"]')[0].text
            article_content = all_content.split('※ 發信站:')[0]
            # print(article_content)
            time.sleep(random.randrange(1,5))

            try:
                with open('./CVSpttArticle/%s.txt' % (title_name), 'w', encoding='utf-8') as f:
                    f.write(article_content)
            except FileNotFoundError:
                with open('./CVSpttArticle/%s.txt' % (title_name.replace('/', '-')), 'w', encoding='utf-8') as f:
                    f.write(article_content)

        except:
            pass

    url = 'https://www.ptt.cc' + soup.select('a[class="btn wide"]')[1]['href']

