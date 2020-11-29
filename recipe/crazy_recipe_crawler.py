import threading
import requests
from bs4 import BeautifulSoup
import time
import json
import os

path = "icook_data"
if not os.path.isdir(path):
    os.mkdir(path)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.116 Safari/537.36 '
}

url = 'https://icook.tw/recipes/'
abnormal_page = {}


def recipe_get_one(cuisine_url):
    res_cuisine = requests.get(url=cuisine_url, headers=headers)
    if res_cuisine.status_code != 200:
        print(f'error, status code: {res_cuisine.status_code}, url: {cuisine_url}')
        return res_cuisine.status_code

    cuisine_soup = BeautifulSoup(res_cuisine.text, 'html.parser')
    # 避免VIP食譜(抓不到資訊)
    if cuisine_soup.select('figure[class="vip-entry vip-entry--responsive"]'):
        return None

    # 食譜名稱
    try:
        recipe = cuisine_soup.select('h1[id="recipe-name"]')[0].text.strip()
    except IndexError:
        return None
    # 輸出正常抓到食譜
    print(f'page get!, {recipe}, url: {cuisine_url}')

    # 讚數
    try:
        like_num = cuisine_soup.select('span[class="stat-content"]')[0].text
    except:
        like_num = '0'
    like_num = like_num.strip('說讚')

    # tag清單製作
    tag_list = []
    try:
        tag_partial = cuisine_soup.select('li[class="recipe-related-keyword-item"]')
        tag_len = (len(tag_partial))

        for i in range(tag_len):
            tag = cuisine_soup.select('li[class="recipe-related-keyword-item"]')[i].select('a')[0].text
            tag_list.append(tag)

    except Exception as e:
        print(f'Error on tags: {e}')

    # 主要圖片
    try:
        main_pic = cuisine_soup.select('div[class="recipe-details"]')[0].select('a')[0]['href']

    except Exception as e:
        print(f'Error on main picture: {e}')

    # 份量
    try:
        quantity = cuisine_soup.select('div[class="servings"]>span')[0].text
    except:
        quantity = 0

    # 時間
    try:
        cook_time_num = cuisine_soup.select('div[class="info-content"]')[1].select('span')[0].text
        cook_time_unit = cuisine_soup.select('div[class="info-content"]')[1].select('span')[1].text
        cook_time = cook_time_num + cook_time_unit
    except:
        cook_time = 'unknown'

    # 材料清單製作
    ingredients_list = []
    ingredients = cuisine_soup.select('div[class="ingredient"]')
    for index, value in enumerate(ingredients):
        ingredients_n = cuisine_soup.select('div[class="ingredient"]')[index].select('a[class="ingredient-search"]')[
            0].text
        ingredients_unit = cuisine_soup.select('div[class="ingredient"]')[index].select('div[class="ingredient-unit"]')[
            0].text
        ingredients_list.append([ingredients_n, ingredients_unit])

    # 步驟字典製作
    step = {}
    step_list = []
    step_pics_list = []
    step_all = cuisine_soup.select('li[class="recipe-details-step-item"]')
    # check step existed
    if step_all:
        for index, value in enumerate(step_all):
            step_num = str(index + 1)
            step_content = value.select('p[class="recipe-step-description-content"]')[0].text.strip().replace('\n',
                                                                                                              '，').replace(
                '\r', '')
            step_list.append('步驟' + step_num + '.' + step_content)

            try:
                if value.select('a'):
                    step_pics = value.select('a')[0]['href']
                    step_pics_list.append(step_pics)
                else:
                    step_pics = ''
                    step_pics_list.append(step_pics)
            except Exception as e:
                print(f'{index}: {e}')
                step_pics = ''
                step_pics_list.append(step_pics)

    else:
        print(f'the step could not find: {cuisine_url}')

    step['content'] = step_list
    step['stepUrl'] = step_pics_list

    # 初始化dictionary
    recipe_dic = {'recipe': recipe, 'tags': tag_list, 'url': cuisine_url, 'like': like_num, 'time': cook_time,
                  'image': main_pic, 'quantity': quantity, 'item': ingredients_list, 'step': step}

    return recipe_dic


def write_in_json(filelist, filename):
    with open(filename, 'w') as f:
        f.write(json.dumps(filelist))


def main(page, content):
    for number in range(page - 39999, page + 1, 1):
        recipe_url = url + str(number)
        recipe = recipe_get_one(recipe_url)

        # 判斷抓的是否為空網頁
        if recipe is None:
            if number % 1000 != 0:
                print(f'page {number} not found.')
                continue
            else:
                pass
        # 回傳如果是status code，代表網頁response不正常，記錄下來
        elif str(recipe).isdigit():
            abnormal_page[recipe_url] = recipe
        else:
            content.append(recipe)

        # 每一千筆且集滿300筆寫入一次json，並清空資料，若該已到最後迴圈亦寫入一次
        if (number % 1000 == 0 and len(content) > 100) or (number == page):
            filename = f'icook_data/icook_recipe{number}.json'
            write_in_json(content, filename)
            content = []
            print(f'page {number - 999} to page {number} done.')
        if number % 200 == 0:
            print(f'{threading.current_thread().name} has processed {number - 199} to {number}.')
        # 當時爬蟲估最後的url
        if number >= 351500:
            break


if __name__ == '__main__':

    start_time = time.time()
    target_page = 40000
    tr = []
    # main(90000,[])
    for i in range(8):
        print(f'Start multithread {i}')
        t = threading.Thread(target=main, args=(target_page, []))
        tr.append(t)
        target_page += 40000

    for i in range(8):
        tr[i].start()
    for i in range(8):
        tr[i].join()

    end_time = time.time()
    print(f"Over, the time use: {end_time - start_time} secs")

    write_in_json(abnormal_page, 'ErrorLog.txt')
