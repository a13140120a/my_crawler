from lxml import etree
import time
import random
import os
from selenium import webdriver
import requests
import json

# 設定資料夾
folder=r'./trplus_sofa'
if not os.path.exists(folder):
    os.mkdir(folder)

headers = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
}
ss = requests.session()

links_xpath = "//div[@id='ProductListSlot']//a[@class='text-secondary gtmImpressions_prod-URL']"
img_xpath = "//div[@class='col-lg-6 photos']/input/@value"
size_content_xpath = "//div[@class='detail-two  product-list__box collapse']//text()"
price_xpath = "//td[@class='prodinfo-mobile-cost-no']/text()"
contents_xpath = "//div[@class='detail-one product-list__box collapse show']//text()"
title_name_xpath = "//div[@class='info__name prod_GDNM']/text()"
id_xpath = "//font[@class='sku prod_GDID']/text()"

def get_HTML(url):
    res = ss.get(url=url, headers=headers)
    get_html = etree.HTML(res.text)
    return get_html

def get_title_name(html):
    title_name = html.xpath(title_name_xpath)[0]
    return title_name

def get_imgList(html):
    imgs = html.xpath(img_xpath)
    img_list = []
    return [img for img in imgs]

def get_size(html):
    # 商品尺寸(無法抓取準確數值)
    size_content = html.xpath(size_content_xpath)
    words = ['CM','*','公分','cm','長','寬','高']
    size = [*filter(lambda x: any(word in x for word in words),size_content)]
    return size

def get_color(html):
    size_content = html.xpath(size_content_xpath)
    title_name = html.xpath(title_name_xpath)[0]
    all_color = []
    if '多' not in title_name:
        try:
            for c in size_content:
                if '顏色:' not in c.strip():
                    color = c.strip().split('：')[1]
                    all_color.append(color)
                elif '顏色：' not in c.strip():
                    color = c.strip().split('：')[1]
                    all_color.append(color)
        except:
            pass
    else:
        try:
            color = title_name.split('-')[1].split('色')[0] + '色'
            all_color.append(color)
        except:
            pass
    return all_color

def get_price(html):
    price = html.xpath(price_xpath)[0].strip()
    return price

def get_id(html):
    id = html.xpath(id_xpath)[0]
    return id

# 內文 Details
def get_details(html):
    details = []
    contents = html.xpath(contents_xpath)
    for content in contents:
        if content.strip() == '':
            pass
        elif '品牌故事' in content.strip():
            break
        elif '注意事項' in content.strip():
            break
        else:
            details.append(content.strip())
    return details

def try_write_to_json(trplus_json):
    title_id = trplus_json.get('id')
    try:
        with open(folder + '/{}.json'.format(title_id), 'w', encoding='utf-8') as f:
            json.dump(trplus_json, f, ensure_ascii=False)
            print('done!')
    except FileNotFoundError:
        with open(folder + '/{}.json'.format(title_id.replace('/', '-')), 'w', encoding='utf-8') as f:
            json.dump(trplus_json, f, ensure_ascii=False)
            print('done!')
    except:
        pass


def Get_Data():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')

    page = 0
    while True:
        tmp_url = 'https://www.trplus.com.tw/TR_Furniture/c/EC_10000011?page={}'
        url = tmp_url.format(page)
        browser.get(url)

        links = browser.find_elements_by_xpath(links_xpath)
        print("link:",links)

        if links == []:
            browser.quit()
            options = webdriver.ChromeOptions()
            #options.add_argument('--headless')
            browser = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
            time.sleep(random.uniform(10, 15))

            url = tmp_url.format(page)
            browser.get(url)
            links = browser.find_elements_by_xpath(links_xpath)

        for link in links:

            # 找含有內文的網址
            content_url = link.get_attribute('href')
            #print(content_url)

            # 標題名稱
            try:
                html = get_HTML(content_url)
                title_name = get_title_name(html)
                img_list = get_imgList(html)
                size = get_size(html)
                all_color = get_color(html)
                price = get_price(html)
                id = get_id(html)
                title_id = 'trp' + str(id)
                details = get_details(html)
                
                trplus_json = {'id': title_id,
                               'title': title_name,
                               "Product number": id,
                               'color': all_color,
                               "jpg": img_list,
                               'price': price,
                               'url': content_url,
                               'Product Information': details,
                               'size': size
                               }
                # 寫入json
                try_write_to_json(trplus_json)
            except IndexError:
                print('此頁面不存在')
                pass
            print("-----------------------")
        print('page:', page, 'len:', len(links), 'finish!!!!')
        page = page + 1
        print("=======================================")
        if page == 120:
            break
        time.sleep(random.uniform(5, 10))


if __name__ == '__main__':
    Get_Data()
