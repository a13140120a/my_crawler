# -*- coding: gbk -*-
from datetime import date
from pathos.pools import ProcessPool as Pool  # using mutiprocessing in class
import os
import json
import time
import pymongo
import requests
import random


client = pymongo.MongoClient("mongodb://192.168.1.25:27017/")

db = client['Topic_104']

mycol = db["NewJobs"]

with open("./newip.txt", "r")as f:
    ip = [*set(f.read().split("\n"))]
    ip.remove("")  # 去除空白行
    random.shuffle(ip)  # 隨機抽選ip

class crowler_104():

    def __init__(self, page= 1, area = ""):
        self.url       = "https://www.104.com.tw/jobs/search/list?ro=0&order=11&asc=0&page=0&jobsource=2018indexpoc"

        self.headers   = {
                        'user-agent'   : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
                        'Referer'      : 'https://www.104.com.tw/job/',
                        'Content-Type' : 'application/json'
                        }

        self._params   = {
                         'page'     : page,  # 搜尋頁數
                         'area'     : area,  # 指定區域
                         'isnew'    : 0,
                          }

        self.proxies   = {"https": ""}

        self.filename  = f'./index/{time.strftime("%Y-%m-%d")}.json'

        self.pool      = Pool(os.cpu_count())



    def try_reqursts(self,area):

        params = self._params.copy()

        while True:
            try:

                params["area"] = area

                res = requests.get(
                    url     =self.url,
                    headers =self.headers,
                    proxies =self.proxies,
                    params  = params,

                )
                break
            except:
                # change ip if Blocked
                global ip
                self.proxies = {"https": ip.pop()}
                print(f"change ip : {self.proxies}")
        return res


    def crowl_index(self, area):

        res = self.try_reqursts(area)

        totalpage = int(res.json()["data"]["totalPage"])

        if totalpage == 0:
            return []

        datalist = []

        #避免出現爭奪記憶體的問題
        params = self._params.copy()

        for i in range(1,totalpage+1):

            params["page"] = i

            res = requests.get(
                url=self.url,
                headers=self.headers,
                params=params
            )

            for job in res.json()["data"]["list"]:

                index5 = job["link"]["job"].split('?')[0].split('/')[-1]

                if index5 != "trans_job_to_case.cfm":

                    datalist.append(index5)

        print("area: {}, totalpage : {}".format(area,totalpage))

        return datalist


    def MutipleCrowl(self,arealist=[]):

        indexlist     = []

        queue = self.pool.map(self.crowl_index,arealist)

        for innerlist in queue:
            for index5 in innerlist:
                indexlist.append(index5)

        del queue

        return indexlist


    def save_to_IndexJson(self,indexlist):

        os.makedirs('./index/', exist_ok=True)

        indexlist = os.listdir('./index/')

        for i in indexlist:
            print('./index/' + i)

            with open('./index/' + i, 'r', encoding='utf-8') as f:
                tmpJsonStr2 = f.read()

                existindex = [i for i in json.loads(tmpJsonStr2)]

        existindex = set(existindex)  # 去重複值

        # 取出不重複的部分
        distinctlist = [*set(indexlist).difference(existindex)]

        with open(self.filename,"w") as f:
            f.write(json.dumps(distinctlist))

        print("Save Successfully!!")


    def load_IndexJson(self):

        with open(self.filename,"r") as f:

            tmplist = [*set(json.loads(f.read()))]  #去重複值

            return tmplist

    def crowl_data(self,index):

        while True:
            try:

                res = requests.get(
                    url     =self.url+index,
                    headers =self.headers,
                    proxies =self.proxies,
                )
                break
            except:
                # change ip if Blocked
                global ip
                self.proxies = {"https": ip.pop()}
                print(f"change ip : {self.proxies}")

        global mycol

        if res.json() == {}:
            pass

        else:

            try:
                mycol.insert_one({"_id": index, "data": res.json()})
                print("insert successfully!：", index)
            except pymongo.errors.DuplicateKeyError:
                pass

    def MutiCrowlData_to_mongo(self,indexlist):

        self.url = "https://www.104.com.tw/job/ajax/content/"

        self.pool.map(self.crowl_data,indexlist)

        print("All Done!!")
