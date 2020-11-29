import requests
from bs4 import BeautifulSoup
from lxml import etree

data = {}
proxy = {}
url = "https://www.mobile01.com/topicdetail.php?f=360&t=6178771"
ua = '''user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'''
header = {}
for i in ua.split('\n'):
    header[i.split(': ')[0]] = i.split(': ')[1]
ss = requests.session()
res = ss.get(url = url,headers=header)

html = etree.HTML(res.text)
a = html.xpath('//div[@itemprop="articleBody"]/text()')
print(a)

##########################      xpath    #####################################################


# 取出所有元素(包含節點、屬性跟內容)
# "//*"
# 星號 (*) 僅能表示未知的元素，但不能表示未知的層級。
# 取得含有屬性的所有 <span>
# "//span[@*]"
# 取得 class 屬性為 "tocnumber" 的所有 <span>
# "//span[@class='tocnumber']"
# 取得 class 屬性非 "tocnumber" 的所有 <span>
# "//span[@class!='tocnumber']"
# or
# "//span[not(@class='tocnumber')]"
# 取得 class 屬性為 "tocnumber" 的第一個 <span>
# "(//span[@class='tocnumber'])[1]"
# 取得 class 屬性為 "toc" 的所有 <div> 其底下 class 屬性為 "tocnumber" 的所有 <span>
# "//div[@class='toc']//span[@class='tocnumber']"
# 取得 class 屬性為 "toc" 的所有 <div> 其底下除第一子階層外 class 屬性為 "tocnumber" 的所有 <span>
# "//div[@class='toc']/*//span[@class='tocnumber']"
# 取得 class 包含 "toclevel-1" 的所有 <li>
# "//li[contains(@class, 'toclevel-1')]"
# 取得 class 不包含 "toclevel-1" 的所有 <li>
# "//li[not(contains(@class, 'toclevel-1'))]"
# 取得包含 id 屬性的所有 <div>
# "//div[@id]"
# 取得不包含 id 屬性的所有 <div>
# "//div[not(@id)]"
# 取得包含 href 屬性的所有元素
# "//*[@href]"
# 取得 class 包含 "toclevel-3" 及 "tocsection-8" 的所有 <li>
# "//li[contains(@class, 'toclevel-3') and contains(@class, 'tocsection-8')]"
# 取得 class 包含 "toclevel-1" 或 "toclevel-2" 的所有 <li>
# "//li[contains(@class, 'toclevel-1') or contains(@class, 'toclevel-2')]"
# 取得內容為 "歷史" 的所有 <span>
# "//span[text(🙁'歷史']"
# 取得內容包含 "HTML" 的所有 <span>
# "//span[contains(text(), 'HTML')]"
# 取得內容包含 "HTML"（不分大小寫）的所有 <span>
# "//span[contains(translate(text(), 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ'), 'HTML')]"
# 在某個已取得的特定元素下，取得該元素底下所有 <li>。
# ".//li"
# 此小數點很容易被忽略，尤其我們被習慣誤導的時候。
#
# 取得 <li> 底下 <a> 的 href 有包含 "HTML" 的 <ul>
# "//ul[li/a[contains(@href, 'HTML')]]"
# 取得下層子元素的 <a> 的 href 有包含 "HTTP" 的 <ul>
# "//ul[*/a[contains(@href, 'HTTP')]]"
# 取得所有子元素的 <a> 的 href 有包含 "SGML" 的 <ul>
# "//ul[.//a[contains(@href, 'SGML')]]"
# 選取body下price元素值大於35的div節點
# xpath(‘/body/div[price>35.00]’)