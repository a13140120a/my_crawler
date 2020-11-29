import requests
import json
import os
from urllib import request #可以下載圖片

ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36'

header = {'User-Agent':ua}


url = 'https://pgw.udn.com.tw/gw/photo.php?u=https://uc.udn.com.tw/photo/2020/06/09/99/8004813.jpg'#其中30篇文章

#print(dcardjson[0].keys())



try:
    request.urlretrieve(url, './456.jpg')  #左邊接url 右邊接放置路徑
except Exception as e:
    print(e)

# try:
#     with open("./123.jpg","wb") as f:#如果遇到錯誤才用此方法
#         urlres = requests.get(url,headers = header)#記得requests有s
#         f.write(urlres.content)
# except Exception as e:
#     print(e)