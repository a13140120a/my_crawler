import requests
from lxml import etree
import re
import json
import pprint

header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

url = 'https://www.google.com/search?q=柴犬&tbm=isch&ved=2&bih=1500'
ss = requests.session()
res = ss.get(url = url,headers= header)
html = etree.HTML(res.text)

a = html.xpath('//script/text()')

for i in a :
    if "AF_initDataCallback(" in i:

        d = re.search('AF_initDataCallback\((.*)\)',i,re.S).group(1)
        d2 = re.findall("(https://.*?\.jpg)",d)
        print(len(d2))
        for j in d2:
            if r"\u003" not in j:
                print(j)

        print("="*60)
        print("="*60)

