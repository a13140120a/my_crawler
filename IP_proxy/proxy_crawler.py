import requests
from lxml import etree
import re
import base64
from multiprocessing import Pool,Manager,Process,Queue
import os

ip = []

def make_iplist(ip):
    def wrapper2(func):
        def wrapper():
            ip.extend(func())
            return func()
        return wrapper
    return wrapper2


@make_iplist(ip)
def crawler1():

    data = {}
    proxy = {}
    ip1 = []
    url = "https://hidemy.name/en/proxy-list/?type=s#list"

    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

    ss = requests.session()

    res = ss.get(url = url,headers=header)

    html = etree.HTML(res.text)
    ip = html.xpath('/html/body/div/div/div/div/table/tbody/tr/td[1]/text()')
    port = html.xpath('/html/body/div/div/div/div/table/tbody/tr/td[2]/text()')

    for i,j in zip(ip,port):
        xx = "https://"+i+":"+j
        ip1.append(xx)
    return ip1

@make_iplist(ip)
def crawler2():
    data = {}
    proxy = {}
    ip2= []
    url = "https://proxy-list.org/english/search.php?search=ssl-yes&country=any&type=any&port=any&ssl=yes&p={}"
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

    ss = requests.session()
    for p in range(1,4):

        res = ss.get(url = url.format(p),headers=header)
        html = etree.HTML(res.text)
        row_ips = html.xpath('//*[@id="proxy-table"]/div/div/ul/li/script/text()')

        for row_ip in row_ips :

            pattern = re.match("Proxy\(\'(.*)\'\)",row_ip).group(1)

            pattern2 = str(base64.b64decode(pattern))

            pattern3 = re.sub("b|\'","",pattern2)

            complete_ip = "https://"+pattern3

            ip2.append(complete_ip)

    return ip2

@make_iplist(ip)
def append_yesterday_ip():   #加上昨天的有效ip
    with open("./newip.txt", "r")as f:
        return f.read().split("\n")

def main(ip,q):
    data = {}
    proxy = {}
    url = "https://www.whatismyip.com.tw/"
    header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
    ss = requests.session()

    if ip.split(":")[0] == "https":
        proxies = {
            "https": i  # 代理ip
        }

        try:
            res = ss.get(url=url, headers=header, proxies=proxies, timeout=15)

            html = etree.HTML(res.text)

            sueecssip = html.xpath('/html/body/b/span/text()')

            q.append(ip)

            print("success:",sueecssip)

        except:

            print("fail to connect! next proxy:",proxies)
            pass


if __name__ == '__main__':
    from functools import partial

    crawler1()
    print("first append:",ip)

    crawler2()
    print("second append:", ip)

    append_yesterday_ip()
    print("third append:", ip)

    ip = [*set(ip)]  #去重複

    del ip[0] #刪除空白

    print("finally ip:",ip)
    print("amount of ip:",len(ip))

    p = Pool(10)

    q = Manager().list()

    main2 = partial(main,q=q)

    p.map(main2,iterable=ip)   #過濾後append到 q 裡面

    p.close()
    p.join()

    with open("./newip.txt", "w")as f2:  #最後寫回newip ，覆蓋昨天的ip
        for i in q:
            f2.write(i)
            f2.write("\n")

    print("Success",q)


