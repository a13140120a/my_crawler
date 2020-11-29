import requests, time ,random, os, json
from bs4 import BeautifulSoup

def saveFile(fileName, fileTitle, article_json, count):

    path = './%s' % fileName

    if not os.path.exists(path):

        os.mkdir(path)

    try:

        with open('%s/%s.txt' % (path, fileTitle), 'w', encoding='utf-8') as w:

            w.write(str(article_json))

    except:

        # 如果title有特殊字元改以網頁名稱+流水號方式儲存
        with open('%s/%s%s.txt' % (path, fileName, count), 'w', encoding='utf-8') as w:

            w.write(str(article_json))


def businessweekiy(endPage, startPage = 1, count = 1):
    '''
    爬取 https://health.businessweekly.com.tw/ 網站
    endPage:爬取頁數
    startPage:開始頁數
    count:流水號起始
    '''
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Referer': 'https://health.businessweekly.com.tw/AArticle.aspx?id=ARTL003003019'}

    count = int(count)  # 流水號

    fileName = 'Business_Weekly_Def'

    for p in range(int(startPage), int(endPage) + 1):

        print('爬網第%d頁，共%d頁' % (p, endPage))

        url = 'https://health.businessweekly.com.tw/BChannel.aspx?Channel_no=0002&s=1&v=1&p=%d' % p

        ss = requests.session()
        res = ss.get(url = url, headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        article = soup.select('div[id="viewcontent"]')[0]
        article = article.select('article')

        for i in article:

            title = i.select('div[class="headline"]')[0]

            i_title = title.select('a')[0].text.split('\r\n')[0]

            i_url = title.select('a')[0]['href']

            print(i_title)
            print(i_url)

            ss = requests.session()
            i_res = ss.get(url=i_url, headers=headers)
            i_soup = BeautifulSoup(i_res.text, 'html.parser')

            #Author
            i_author = i_soup.select('em[class="authorname"]')[0].text
            i_author = str(i_author).lstrip('撰文者')

            #Item
            i_time = i_soup.select('div[class="detail_info right"]')[0].text
            i_time = str(i_time).split('瀏覽數')
            i_time = i_time[0]

            #Content
            i_content = i_soup.select('section[id="articleBlock"]')[0].text

            article_json = {'url': i_url, 'title': i_title, 'lesson': 0, 'strength': 0, 'lesson_time': 0, 'describe': i_content,
                            'time': i_time, 'author': i_author}

            #Dict 包含中文
            article_json = json.dumps(article_json, ensure_ascii=False)

            saveFile(fileName, i_title, article_json, count)

            count += 1


if __name__ == '__main__':
    businessweekiy(292)





