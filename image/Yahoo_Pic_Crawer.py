import time
import requests
import urllib
from lxml import etree
import os
import random


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

#請求連接yahoo圖片搜尋網頁，擷取圖片url，並下載圖片
def GetYahooImag(search_item,path):

    #用來進行圖片編號
    m=1

    #定義空list，儲存圖片url
    img_urls = []

    for num in range(1, 35):
        url = 'https://tw.images.search.yahoo.com/search/images?n=60&ei=UTF-8&fr=sfp&fr2=sb-top-tw.images.search&o=js&p={}&tmpl=&nost=1&b={}&iid=Y.{}'.format(search_item,60*num+1,num)
        print('正在連接：'+ '第' + str(num) + '頁：' + url)

        try:
            ss = requests.session()

            # 發送get請求
            res = ss.get(url=url, headers=headers)
            print('get請求狀態：', res.status_code)

            #擷取data-src屬性
            html = etree.HTML(res.json()["html"])
            src = html.xpath('//img/@data-src')

            #下載圖片(判定圖片url是否重複，避免重複下載)
            for img_url in src:
                if img_url not in img_urls:
                    img_urls .append(img_url)
                    print('*******' + "儲存第{}照片url：".format(m) + '*******')
                    print(img_url)

                    try:
                        filename = str(m) + '_' + search_item + '_' + '.jpg'
                        urllib.request.urlretrieve(img_url, os.path.join(path, filename))
                        m += 1
                        time.sleep(float(random.randint(100, 200)) / 200)
                    except Exception as e:
                        pass
                        print(e)
                else:
                    print("！！！此照片url已重複！！！")
        except Exception as g:
            pass
            print(g)

    # 每抓取50張圖片休息3~5秒
    time.sleep(1 + float(random.randint(400, 800)) / 200)

def main():
    #計算爬蟲程式執行時間(起點)
    start = time.time()

    # 輸入搜尋標題，定義圖片儲存路徑，若無此路徑，創建該資料夾
    search = ['藥球','壺鈴','推肩機','推肩器','肩推器','登山機','飛輪健身','牧師椅','橢圓交叉訓練機']

    for i in search:
        local_path = r'C:\Users\Big data\PycharmProjects\NewProject\yahoo_pic_request\{}'.format(i)
        if not os.path.exists(local_path):
            os.mkdir(local_path)
        print(local_path)
        GetYahooImag(i, local_path)
        time.sleep(6 + float(random.randint(400, 800)) / 200)

    #計算爬蟲程式執行時間(終點)
    end = time.time()
    spend = end - start
    hour = spend // 3600
    minu = (spend - 3600 * hour) // 60
    sec = spend - 3600 * hour - 60 * minu
    print(f'一共花費了{hour}小時{minu}分鐘{sec}秒')

if __name__ == '__main__':
    main()
    print('Download complete!')