import time, random, pymongo
import requests
import os
import pandas as pd
from bs4 import BeautifulSoup
import sys


user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
headers = {'User-agent' : user_agent}
allrecipe_rul = 'https://www.allrecipes.com/search/results/?wt={}&sort=re&page={}'


# Conneting to MongoDB
Client = pymongo.MongoClient(host='localhost', port=27017)


def getRecipeList(keyword, page):

    os.makedirs('./allrecipe_{}/'.format(keyword), exist_ok=True)

    init_url = allrecipe_rul.format(keyword, 1)
    ss = requests.session()
    response = ss.get(init_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    recipe_list = []

    result_content = soup.select('div.results-container')
    for content in result_content:
        result_number = content.select('span.subtext')
        result = int(result_number[0].text.split(' ')[0])
        print("There are {} recipes".format(result))
    available_pages = result // 20

    # Check if user input valid page number
    if page > available_pages:
        print('There are only {} pages of result'.format(available_pages))
        searching_page = available_pages
    else:
        searching_page = page
    time.sleep(random.randrange(3,7))

    print('Total searching pags are {}'.format(searching_page))

    # Extracting recipes URLs
    recipe_list_dcit = {}
    for n in range(searching_page):
        searching_url = allrecipe_rul.format(keyword, n+1)
        response_2 = ss.get(searching_url, headers=headers)
        soup_2 = BeautifulSoup(response_2.text, 'html.parser')
        all_urls = soup_2.select('div.fixed-recipe-card__info')
        for content in all_urls:
            find_url = content.select('a')
            url = find_url[0]['href']
            title = find_url[0].text.strip()
            recipe_list_dcit[url] = title

    # Creating cach file

    with open('./allrecipe_search_cach.txt'.format(keyword), 'a', encoding='utf-8') as file:
        file.close()

    return recipe_list_dcit


def getRecipeIngredient(keyword, recipe_dict):
    print('Starting to scrap recipes....')
    for url in list(recipe_dict.keys()):
        content_dict = {}

        # First, refering to cach
        with open('./allrecipe_search_cach.txt'.format(keyword), 'r') as check_cach:
            cach_content = check_cach.read()
        # checking if the recipe has already been in files
        if url in cach_content:
            print('Recipe {} has been saved before !!..'.format(url))
            pass

        else:
            try:
                title = result_dict[url]
                ss = requests.session()
                response = ss.get(url, headers=headers)
                soup = BeautifulSoup(response.text, 'html.parser')

                # Extracting ingredients
                ingredient_str = ''
                ingredient_section = soup.select('ul.ingredients-section')
                for item in ingredient_section:
                    ingredient_item = item.select('li.ingredients-item')
                    for ingredient in ingredient_item:
                        name = ingredient.select('span.ingredients-item-name')
                        ingredient_str = ingredient_str + name[0].text.strip() + ','


                author_info = soup.select('div.author-text')
                for info in author_info:
                    name_title = info.select('span.author-name-title')
                    for names_info in name_title:
                        name = names_info.select('a')
                        author = name[0].text


                step_str = ''
                reciep_content = soup.select('div.recipe-content-container')
                for content_info in reciep_content:
                    layer2 = content_info.select('section.recipe-instructions.recipe-instructions-new.component.container')
                    for layer3 in layer2:
                        layer4 = layer3.select('fieldset.instructions-section__fieldset')
                        for layer5 in layer4:
                            steps = layer5.select('div.section-body')
                            for step_detail in steps:
                                step_str = step_str + step_detail.text.strip() + '|'
                try:
                    content_dict['url'] = url
                    content_dict["title"] = title
                    content_dict["time"] = 0
                    content_dict["author"] = author
                    content_dict["ingredient"] = ingredient_str
                    content_dict["steps"] = step_str
                    content_dict["comment"] = 0
                    content_dict["category"] = 'EN_' + keyword

                except Exception as error_name_1:
                    print(error_name_1)
            # saveFile(content_dict, keyword, url)
            except Exception as error_name_3:
                print(error_name_3)
                pass

            try:
                db = Client.tibame
                collection = db.recipe_raw_en
                insert_item = content_dict
                insert_result = db.recipe_raw_en.insert_one(insert_item)
                print(insert_result)
                saveFile(content_dict, keyword, url)

            except Exception as error_name_2:
                print(error_name_2)
                pass




def saveFile(content_dict, directory, url):
    '''
    Output recipe as txt file, with json format
    :param content_dict: A dictionary, containing each recipe
    :param directory: A string, specifying working directory for file saving
    :param item_no: A string, specifying file name in accordance with recipe web_id
    :return: No returning object, saving into text file instead
    '''
    try:
        # Extracting each recipe id
        item_no = url.split('/')[4]
        # Save recipe into file
        with open('./allrecipe_{}/{}.txt'.format(directory, item_no), 'w', encoding='utf-8') as file:
            file.write(str(content_dict))
        # writing recipe_id into cach
        with open('./allrecipe_search_cach.txt'.format(directory), 'a', encoding='utf-8') as cach:
            cach.write(url+'\n')
        print('Recipe "{}" saved !'.format(item_no))
    except Exception as error_name:
        print(error_name)
        pass



if __name__ == '__main__':

    #使用者自行輸入
    searching_list = sys.argv

    for item in searching_list:
        result_dict = getRecipeList(item, 800)
        getRecipeIngredient(item,result_dict)