# coding=gbk
from datetime import date
from multiprocessing import Pool,managers
import os
import json
import time
import pymongo
import requests


client = pymongo.MongoClient("mongodb://192.168.1.25:27017/")

db = client['Topic_104']

mycol = db["NewJobs"]

filename = f'./index/{time.strftime("%Y-%m-%d")}.json'

#open url list
def getindexlist():

    global filename

    if os.path.isfile(filename):
        file = open(filename,"r")
        todayindexlist = json.loads(file.read())
        return todayindexlist
    else:
        print("No index today!")

def crowl(url):
    tmpdict = {}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
    'Referer': 'https://www.104.com.tw/job/'}

    ss=requests.session()
    res = ss.get(url= url , headers = headers)

    if res.status_code == 200:
        try:
            return res.json()
        except json.decoder.JSONDecodeError:
            print("No data")

    else:
        print('請求網頁json錯誤, 錯誤狀態碼：', res.status_code)


def crowler_to_mongo(index):
    if len(index) < 10 :
        url = "https://www.104.com.tw/job/ajax/content/"+index
        try:
            datajson = crowl(url)
            write_to_mongo(index,datajson)
        except Exception as e:
            print("error:",e)
            time.sleep(2)
    else:
        pass

def write_to_mongo(index,CACHE_DICTION):
    global mycol
    if CACHE_DICTION == {}:
        pass
    else:
        mycol.insert_one({ "_id" : index, "data" : CACHE_DICTION })
        print("insert successfully!：",index)


if __name__ == '__main__':

    list = getindexlist()

    p = Pool(8)

    try:
        p.map(crowler_to_mongo,iterable=(i for i in list))
    except:
        print("Error:Good bye!")

    p.close()

    p.join()
