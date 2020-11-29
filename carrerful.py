import requests
from bs4 import BeautifulSoup
from lxml import etree
import pprint
#key = input("input")
key = "牛奶"
pagesize = 20
data = {}
proxy = {}
url = "https://online.carrefour.com.tw/ProductShowcase/Commodities/GetSearchJson"
ua = '''User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'''
header = {}
for i in ua.split('\n'):
    header[i.split(': ')[0]] = i.split(': ')[1]
param = {'key': key,
'orderBy': 0,
'pageIndex': 0,
'pageSize': pagesize,
'minPrice': '',
'maxPrice': '',
'categoryId': '',
'isLoadCate': 'false',
'manufacturerId': 0,
'topManufacturerName': '',
'isBrandAll': 'false'}
ss = requests.session()
res = ss.post(url = url,headers=header,params = param)
a = res.json()
count = a["content"]["Count"] #總筆數

for i in range(1,count // pagesize+2) :
    print(i)
    param['pageIndex'] = i
    res = ss.post(url=url, headers=header, params=param)
    b = res.json()
    for j in b["content"]["ProductListModel"] :
        print(j["Name"],": $",j["Price"],)
print("===================end========================")

url = 'https://www.costco.com.tw/search?text={}'.format(key)

costco = requests.get(url,header)

html = etree.HTML(costco.text)
a = html.xpath('//*[@id="list-view-id"]/li/div/div/div/a/span/text()')
b = html.xpath('//*[@id="list-view-id"]/li/div/div/div/div/span/span/text()')
for i,j in zip(a,b) :
    print(i,": $",j)

urlpx = 'https://shop.pxmart.com.tw/webapi/SearchV2/GetShopSalePageBySearch?keyword={}&minPrice=&maxPrice=&shippingType=&payType=&order=Correlation&startIndex=0&maxCount=50&displayScore=&shopCategoryId=&scoreThreshold=0.8&isResearch=true&v=0&shopId=2&lang=zh-TW'.format(key)
print("===================end========================")

res2 = requests.get(urlpx,header)
header.update({'referer': 'https://shop.pxmart.com.tw/v2/Search'})
totalpage = int(res2.json()["Data"]["TotalSize"])//50 + 1
print(totalpage)

for i in res2.json()["Data"]["SalePageList"]:
    print(i["Title"].split('】')[-1],": $",int(i['Price']))