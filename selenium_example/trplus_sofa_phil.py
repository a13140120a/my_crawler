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



def get_HTML(url):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'
    }
    ss = requests.session()
    res = ss.get(url=url, headers=headers)
    get_html = etree.HTML(res.text)   # 利用etree.HTML把字串解析成HTML文件
    return get_html

def Get_Data():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    browser = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')

    page = 0
    while True:

        tmp_url = 'https://www.trplus.com.tw/TR_Furniture/c/EC_10000011?page={}'
        url = tmp_url.format(page)
        browser.get(url)
        links = browser.find_elements_by_xpath("//div[@id='ProductListSlot']//a[@class='text-secondary gtmImpressions_prod-URL']")
        print("link:",links)

        if links == []:
            browser.quit()
            options = webdriver.ChromeOptions()
            #options.add_argument('--headless')
            browser = webdriver.Chrome(chrome_options=options, executable_path='./chromedriver')
            time.sleep(random.uniform(10, 15))

            tmp_url = 'https://www.trplus.com.tw/TR_Furniture/c/EC_10000011?page={}'
            url = tmp_url.format(page)
            browser.get(url)
            links = browser.find_elements_by_xpath("//div[@id='ProductListSlot']//a[@class='text-secondary gtmImpressions_prod-URL']")



        for link in links:

            # 找含有內文的網址
            content_url = link.get_attribute('href')
            #print(content_url)

            # 標題名稱
            try:
                title_name = get_HTML(content_url).xpath("//div[@class='info__name prod_GDNM']/text()")
                title_name = title_name[0]
                #print(title_name)

                # 照片
                imgs = get_HTML(content_url).xpath("//div[@class='col-lg-6 photos']/input/@value")
                img_list = []
                for img in imgs:
                    img_list.append(img)
                #print('imgs done!!')
                # 商品尺寸(無法抓取準確數值)
                size_content = get_HTML(content_url).xpath("//div[@class='detail-two  product-list__box collapse']//text()")
                size = []
                for s in size_content:
                    #print (s.strip())
                    if s.strip().find('CM') != -1:
                        size.append(s.strip())
                    elif s.strip().find('*') != -1:
                        size.append(s.strip())
                    elif s.strip().find('公分') != -1:
                        size.append(s.strip())
                    elif s.strip().find('cm') != -1:
                        size.append(s.strip())
                    elif s.strip().find('長') != -1:
                        size.append(s.strip())
                    elif s.strip().find('寬') != -1:
                        size.append(s.strip())
                    elif s.strip().find('高') != -1:
                        size.append(s.strip())

                all_color = []
                if title_name.find('多') != -1:
                    try:
                        for c in size_content:
                            if c.strip().find('顏色:') != -1:
                                color = c.strip().split('：')[1]
                                all_color.append(color)
                            elif c.strip().find('顏色：') != -1:
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
                #print('color done!!')

                # 商品價格
                price = get_HTML(content_url).xpath("//td[@class='prodinfo-mobile-cost-no']/text()")
                price = price[0].strip()
                #print('price done!!')
                # 商品ID

                id = get_HTML(content_url).xpath("//font[@class='sku prod_GDID']/text()")

                title_id = 'trp' + str(id[0])
                #print('title_id done!!')
                # 內文 Details
                details = []
                contents = get_HTML(content_url).xpath("//div[@class='detail-one product-list__box collapse show']//text()")
                for content in contents:
                    if content.strip() == '':
                        pass
                    elif '品牌故事' in content.strip():
                        break
                    elif '注意事項' in content.strip():
                        break
                    else:
                        details.append(content.strip())
                #print('details done!!')
                trplus_json = {'id': title_id,
                               # "type": title_type,
                               'title': title_name,
                               "Product number": id[0],
                               'color': all_color,
                               "jpg": img_list,
                               # "summary": title_summary,
                               'price': price,
                               'url': content_url,
                               'Product Information': details,
                               'size': size
                               }

                #print(trplus_json)
                # 寫入json
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