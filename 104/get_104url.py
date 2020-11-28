from multiprocessing import Pool, Manager, Queue
import re, time, requests, os
from lxml import etree
import json
import random
import pprint



proxies = {"https": ""}

#取得area list以便多程序執行



def get_iplist():
    with open("./newip.txt", "r")as f:
        ip = [*set(f.read().split("\n"))]
        ip.remove("")  #去除空白行
        random.shuffle(ip)  #隨機抽選ip
        return ip

def get_arealist():
    with open("104area.txt", "r")as f:
        a = f.read()
    return a.split("\n")


def crawl_index(area, q,i):
    global proxies
    ss = requests.session()
    x = 0
    my_params = {'page': 1,  # 搜尋參數
                 'area': area,  # 指定區域
                 #'isnew': 0
                 }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
        'Referer': 'https://www.104.com.tw/job/',
        'Content-Type': 'application/json'
    }
    searchpageurl = 'https://www.104.com.tw/jobs/search/list?ro=0&order=11&asc=0&page=0&jobsource=2018indexpoc'
    while True:
        try:
            res = ss.get(
                url=searchpageurl,
                headers=headers,
                params=my_params,
                proxies=proxies)

            break
        except Exception as e:

            proxies = {"https": i.pop()} #被鎖就更換ip

            print("change ip:", proxies)

            continue

    totalpage = int(res.json()["data"]["totalPage"])


    for page in range(1,totalpage+1):

        my_params["page"]=page

        print (f'area:{area}, page:{page}, PID:{os.getpid()}')

        res = ss.get(url=searchpageurl, headers=headers, params=my_params, proxies=proxies)

        for job in res.json()["data"]["list"]:
            index5 = job["link"]["job"].split('?')[0].split('/')[-1]
            if index5 != "trans_job_to_case.cfm":
                q.append(index5)



def distinct_index(nexindexlist):
    existindex = []
    os.makedirs('./index/', exist_ok=True)
    indexlist = os.listdir('./index/')
    for i in indexlist:

        print('./index/' + i)

        with open('./index/' + i, 'r', encoding='utf-8') as f:
            tmpJsonStr2 = f.read()
            for i in json.loads(tmpJsonStr2):
                existindex.append(i)

    existindex = set(existindex)  #去重複值

    #取出不重複的部分
    parelist = [*set(nexindexlist).difference(existindex)]

    return parelist


if __name__ == '__main__':

    arealist = get_arealist()

    del arealist[-1]


    print(arealist)

    todayindexlist = []

    start = time.time()

    print("collecting index....")


    iplist = get_iplist()


    manager = Manager()

    q  = manager.list() #存放url的list

    ip = manager.list(iplist) #存放ip的list

    from functools import partial

    p = Pool(8)

    crawl_index2 = partial(crawl_index, q=q,i=ip)

    res = p.map(crawl_index2,iterable=arealist)
    res = [r for r in res if r is not None]  #避免輸入值為None會出錯

    p.close()
    p.join()

    print("index count:", len(q))

    todayindexlist = distinct_index(q)  # 比對並且去重複

    print("distinct index count:", len(todayindexlist))
    print(todayindexlist)

    with open(f'./index/{time.strftime("%Y-%m-%d")}.json',"w") as f:  #存檔
        f.write(json.dumps(todayindexlist))

    print(f"done!!!,spend time {time.time()-start} second ...")
