import requests
from bs4 import BeautifulSoup
import os
import json
import time
import pprint

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"

headers = {'User-agent' : user_agent}



def Get_Lastest_Article_ID():

    Main_Url = 'https://www.dcard.tw/f?latest=true'
    Main_Response = requests.get(Main_Url, headers=headers)
    soup = BeautifulSoup(Main_Response.text, "html.parser")
    Lastest_Article_Row_ID = soup.select('#__next > div > div > div > div > div > div > div > div > div > div > article > h2 > a')[0]["href"]
    Lastest_Article_ID = Lastest_Article_Row_ID.split("/")[-1]
    return int(Lastest_Article_ID)

def Get_Json_Requests(before):


    Json_Url = "https://www.dcard.tw/service/api/v2/posts?limit=100&before={}".format(before)

    Response = requests.get(Json_Url, headers=headers)

    return Response




def Craw_Html_List(before):


    Response_Json = Get_Json_Requests(before).json()

    while Response_Json != []:

        Finall_json = []

        Response_Json = Get_Json_Requests(before).json()

        for i in Response_Json:

            content_id = i['id']
            classify = i["forumAlias"]
            Html_Url = "https://www.dcard.tw/f/{classify}/p/{content_id}".format(content_id=content_id,classify=classify)
            Html_Response = requests.get(Html_Url, headers=headers)
            soup = BeautifulSoup(Html_Response.text, "html.parser")
            content_title = soup.select("div>div>div>div>div>div>div>article>div>div>h1")

            try:
                Row_Content_Time = soup.select("div>div>div>div>div>div>div>article>div>div")
                Content_Time = Row_Content_Time[2].text
            except:
                Row_Content_Time = '無'
                Content_Time = Row_Content_Time

            try:
                Row_Content_Content = soup.select("div>div>div>div>div>div>div>article>div>div>div")
                Content_Content = Row_Content_Content[0].text

            except IndexError:
                Row_Content_Content = '無'
                Content_Content = Row_Content_Content

            fitness_json_dict = {}
            value = {'url' : Html_Url,
                     'title' : content_title[0].text,
                     'describe' : Content_Content,
                     'time': Content_Time
                     }

            Finall_json.append(value)


        SaveFile()
        before -= 100
        print(Finall_json)


def SaveFile(fileName,data):

    try:
        with open('./dcard/%s.json' % fileName, 'w', encoding='utf-8') as w:
            w.write(json.dumps(data))

    except Exception as e:
        print("Error:",e)



if __name__ == '__main__':

    os.makedirs('./dcard/', exist_ok=True)

    #取得最新文章id
    before = Get_Lastest_Article_ID()

    Craw_Html_List(before)

