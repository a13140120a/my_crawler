import requests
import pprint
from pyquery import PyQuery as pq


ua = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
'Referer':'http://free-proxy.cz/en/proxylist/main/1',
}


url = 'https://www.ytower.com.tw/recipe/'
ss = requests.session()
res = ss.get(url = url,headers=ua)
res.encoding = res.apparent_encoding


doc = pq(res.text)
a = pq(res.text)('a')  #doc('a')

#-------------------找到所有a節點的href屬性(none也會印出來)-----
#print(a.items())
m = []
for item in a.items():
    print(item.attr('href'))
    m.append(item.attr('href'))
    #print(item.add_class('addclass'))  #新增屬性class="addclass"  (用途不明)
print(m)
#print(type(m[0]))

#----------------------------把所有節點變成字串----------------------------------
print(a.text())


#-------------使用.(class)和#(id)來查找節點-----------------------------------------
#print(doc('.step'))
#print(doc('.step').text())    #加.text() 去標籤

li = pq(res.text)('li')
#print(li.text())
#print(doc('li').eq(2))


