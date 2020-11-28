import requests
from lxml import etree
import re

a = 2
b = 5
v = 3
c = 1
q = 0
r = 8
l = 9
w = 6
m = 4
i = 7



header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}




def deal_port(string):

    match = {
        "a": 2,
        "b": 5,
        "c": 1,
        "v": 3,
        "q": 0,
        "r": 8,
        "l": 9,
        "w": 6,
        "m": 4,
        "i": 7
    }
    pattern = re.search(r"\(\"\:\"\+(.*?)\)",string).group(1)

    port_list = pattern.split("+")

    port = map(lambda x:str(match.get(x)),port_list)

    return "".join([*port])



if __name__ == '__main__':

    iplist = set()

    for page in range(1,11):

        url = "http://www.cnproxy.com/proxy{}.html".format(page)

        ss = requests.session()
        res = ss.get(url=url, headers=header)

        html = etree.HTML(res.text)


        ip = html.xpath('//table//td[1]/text()')
        del ip[0]

        ip_type = html.xpath('//table//td[2]/text()')

        port = html.xpath('//table//td[1]//script/text()')

        for i in zip(ip_type,ip,port):
            print(i)
            if i[0] == "HTTP":
                full_ip = "http://"+i[1]+":"+deal_port(i[2])
                iplist.add(full_ip)

    print(iplist)
    with open("cnproxy_iplist.txt", "w", encoding="utf-8") as f:
        for i  in iplist:
            f.write(i)
            f.write("\n")


