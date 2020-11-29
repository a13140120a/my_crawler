import requests
from bs4 import BeautifulSoup
from urllib import request
import pprint
url = 'https://www.whatismyip.com.tw/'

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'

header = {'User-Agent':ua,
'HTTP_FORWARDED':'',
'HTTP_X_FORWARDED_FOR':'',
'HTTP_CLIENT_IP':'',
'HTTP_VIA':'',
'HTTP_XROXY_CONNECTION':'',
'HTTP_PROXY_CONNECTION':''}

ss = requests.session()
proxy = {
    'http':'http://185.232.65.66:5836',
}

res =  ss.get(url = url,headers = header, proxies = proxy)

soup = BeautifulSoup(res.text, "html.parser")
#print(soup.prettify())
for i in soup.select('b[style="font-size:1.5em;"] > span'):
    print(i.text)

print(soup.select('script')[0]['type'])



#  .class  #id
#-----------好用----------------------------------
# for i , elememt in enumerate(a):
#     print(i)
#     print(elememt.text)
