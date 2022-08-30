# my_crawler

xpath:  [速查表](https://www.itread01.com/content/1547103070.html)  
xpath:  [速查表](http://caibaojian.com/scb/xpath.html)

範例：
```python
import requests
import pprint
from lxml import etree

if __name__ == '__main__':
    header = {}

    if True:
        header["X-Requested-With"] = "XMLHttpRequest"

    session = requests.session()
    res_get = session.get('http://localhost', headers=header)
    # pprint.pprint(res_get.cookies.get_dict())
    html = etree.HTML(res_get.text)
    token = html.xpath('/html/head/meta[@name="csrf-token"]/@content')[0]
    print(token)

    json_body = {
        "email": "admin@example.com",
        "password": "admin123",
        "_token": token
    }

    res_post = session.post('http://localhost/admin/login', headers=header, json=json_body)

    res_quote = session.get('http://localhost/admin/quotes', headers=header)

    with open('result.html', 'w', encoding='utf-8') as f:
        f.write(res_quote.text)
        
    # 從當前節點繼續取其他節點
    target1 = html.xpath('...')
    # 前面加一個點表示當前節點
    target2 = target1.xpath('./a[@class="example"]')
```

```js
取出所有元素(包含節點、屬性跟內容)
"//*"
星號 (*) 僅能表示未知的元素，但不能表示未知的層級。
取得含有屬性的所有 <span>
"//span[@*]"
取得 class 屬性為 "tocnumber" 的所有 <span>
"//span[@class='tocnumber']"
取得 class 屬性非 "tocnumber" 的所有 <span>
"//span[@class!='tocnumber']"
or
"//span[not(@class='tocnumber')]"
取得 class 屬性為 "tocnumber" 的第一個 <span>
"(//span[@class='tocnumber'])[1]"
取得 class 屬性為 "toc" 的所有 <div> 其底下 class 屬性為 "tocnumber" 的所有 <span>
"//div[@class='toc']//span[@class='tocnumber']"
取得 class 屬性為 "toc" 的所有 <div> 其底下除第一子階層外 class 屬性為 "tocnumber" 的所有 <span>
"//div[@class='toc']/*//span[@class='tocnumber']"
取得 class 包含 "toclevel-1" 的所有 <li>
"//li[contains(@class, 'toclevel-1')]"
取得 class 不包含 "toclevel-1" 的所有 <li>
"//li[not(contains(@class, 'toclevel-1'))]"
取得包含 id 屬性的所有 <div>
"//div[@id]"
取得不包含 id 屬性的所有 <div>
"//div[not(@id)]"
取得包含 href 屬性的所有元素
"//*[@href]"
取得 class 包含 "toclevel-3" 及 "tocsection-8" 的所有 <li>
"//li[contains(@class, 'toclevel-3') and contains(@class, 'tocsection-8')]"
取得 class 包含 "toclevel-1" 或 "toclevel-2" 的所有 <li>
"//li[contains(@class, 'toclevel-1') or contains(@class, 'toclevel-2')]"
取得內容為 "歷史" 的所有 <span>
"//span[text(),'歷史']"
取得內容包含 "HTML" 的所有 <span>
"//span[contains(text(), 'HTML')]"
取得內容包含 "HTML"（不分大小寫）的所有 <span>
"//span[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'HTML')]"
在某個已取得的特定元素下，取得該元素底下所有 <li>。
".//li"
此小數點很容易被忽略，尤其我們被習慣誤導的時候。

取得 <li> 底下 <a> 的 href 有包含 "HTML" 的 <ul>
"//ul[li/a[contains(@href, 'HTML')]]"
取得下層子元素的 <a> 的 href 有包含 "HTTP" 的 <ul>
"//ul[*/a[contains(@href, 'HTTP')]]"
取得所有子元素的 <a> 的 href 有包含 "SGML" 的 <ul>
"//ul[.//a[contains(@href, 'SGML')]]"
選取body下price元素值大於35的div節點
xpath(‘/body/div[price>35.00]’)
```
bs4:  [速查表](https://blog.csdn.net/qq_40909410/article/details/100709009)
```js
res =  ss.get(url = url,headers = header, proxies = proxy)
soup = BeautifulSoup(res.text, "html.parser")

.是class
#是id
soup.prettify()#漂亮打印
#select
for i in soup.select('b[style="font"] > span'):
    print(i.text)

print(soup.select('script')[0]['type'])

```

pyquery:
```js

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
```

圖片下載範例:
```js
from urllib import request #可以下載圖片

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'

header = {'User-Agent':ua}

url = 'https://pgw.udn.com.tw/gw/photo.php?u=https://uc.udn.com.tw/photo/2020/06/09/99/8004813.jpg'

try:
    request.urlretrieve(url, './456.jpg')  #左邊接url 右邊接放置路徑
except Exception as e:
    print(e)

#方法2
# try:
#     with open("./123.jpg","wb") as f:
#         urlres = requests.get(url,headers = header)#記得requests有s
#         f.write(urlres.content)
# except Exception as e:
#     print(e)
```
