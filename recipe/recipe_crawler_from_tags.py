'''
以多執行緒爬取食譜網站全站的標籤及其下的網址
'''


import requests
from bs4 import BeautifulSoup
import time
import threading
import queue


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.116 Safari/537.36 '
}

main_page = 'https://icook.tw/categories?ref=icook-footer'


# 爬標籤用
def get_catagories_url(main_page):
    catagories_list = []
    res = requests.get(url=main_page, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    catagories = soup.select('li[class="categories-all-child"]')  # 算出有N類食品(106類)
    for catagories_number in range(len(catagories)):  # N類食品
        catagories_url = "https://icook.tw" + soup.select('a[class="categories-all-child-link"]')[catagories_number][
            'href']
        catagories_list.append(catagories_url)
    return catagories_list


# 爬標籤底下的網址用
def get_cuisine_url(catagories_urls):
    cuisine_url_list = []  # 每類別的所有網址
    list1, list2, list3, list4 = [], [], [], []
    for each_catagory_url in catagories_urls:
        print(f'now is {each_catagory_url}')
        page = 1
        # for p in range(1):
        for p in range(1, 1500):  # 每類N頁
            each_cuisine_page_url = each_catagory_url + f'?page={page}'
            each_cuisine_res = requests.get(url=each_cuisine_page_url, headers=headers)
            catagories_soup = BeautifulSoup(each_cuisine_res.text, 'html.parser')
            page_length = catagories_soup.select('li[class="browse-recipe-item"]')
            if not page_length:  # 若此頁抓不到任何資料，則直接結束迴圈
                break

            for i in range(len(page_length)):  # 每一頁細項
                cuisine_url = "https://icook.tw" + catagories_soup.select('a[class="browse-recipe-link"]')[i]['href']
                print(cuisine_url)
                if (cuisine_url in list1) or (cuisine_url in list2) or (cuisine_url in list3) or (cuisine_url in list4):
                    continue
                if p % 4 == 0:
                    list1.append(cuisine_url)
                elif p % 4 == 1:
                    list2.append(cuisine_url)
                elif p % 4 == 2:
                    list3.append(cuisine_url)
                else:
                    list4.append(cuisine_url)
            page += 1
            print(f'page {page}')
    cuisine_url_list.append(list1)
    cuisine_url_list.append(list2)
    cuisine_url_list.append(list3)
    cuisine_url_list.append(list4)
    return cuisine_url_list


def main():
    start_time = time.time()
    # 先爬下全部tag url
    catagories_urls = get_catagories_url(main_page)
    print(catagories_urls)
    print(f"total number of tags: {len(catagories_urls)}")

    # 把tag url 分配成4份，供後續multithread 爬取時使用
    part_urls = [[] for _ in range(4)]
    sp = 1
    for cu in catagories_urls:
        if sp % 4 == 0:
            part_urls[0].append(cu)
        elif sp % 4 == 1:
            part_urls[1].append(cu)
        elif sp % 4 == 2:
            part_urls[2].append(cu)
        elif sp % 4 == 3:
            part_urls[3].append(cu)
        sp += 1
    print(part_urls)

    # 建立Queue 儲存thread的function return值
    que = queue.Queue()

    print('Start multithread......')
    tr = []
    for i in range(4):
        t = threading.Thread(target=lambda q, arg1: q.put(get_cuisine_url(arg1)), args=(que, part_urls[i]))
        tr.append(t)
    for i in range(4):
        tr[i].start()
    for i in range(4):
        tr[i].join()

    print('Multithread completed.')
    total_recipe_url = []
    for i in range(4):
        total_recipe_url += que.get()
    print(total_recipe_url)
    with open('url_list.txt', 'w')as f:
        for urls in total_recipe_url:
            for url in urls:
                f.writelines(url + ',')

    end_time = time.time()
    print(f"Over, the time use: {end_time - start_time} secs")


if __name__ == '__main__':
    main()
