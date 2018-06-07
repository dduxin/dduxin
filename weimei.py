#-*- coding:utf-8 -*-
"""
百度贴吧 唯美图片的 图片
"""

import os
from urllib import request
import random
import re


L = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'},

    {'User-Agent': 'Mozilla/5.0 (Macintosh; U; \
    Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 \
    (KHTML, like Gecko) Version/5.1 Safari/534.50'},

    {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) \
    AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},

    {'User-Agent': 'Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) \
    Presto/2.8.131 Version/11.11'},

    {'User-Agent': 'Opera/9.80 (Windows NT 6.1; U; en) \
    Presto/2.8.131 Version/11.11'}
]

headers = random.choice(L)


url =  'https://tieba.baidu.com/p/3823765471'
req = request.Request(url, headers=headers)
response = request.urlopen(req)
html = response.read().decode('utf-8')

def cbk(a,b,c):  
    '''''回调函数 
    @a:已经下载的数据块 
    @b:数据块的大小 
    @c:远程文件的大小 
    '''  
    per=100.0*a*b/c  
    if per>100:  
        per=100  
    print ('%.2f%%' % per)

# <img class="BDE_Image" src="https://imgsa.baidu.com/forum/w%3D580/sign=f9cf09409c25bc312b5d01906ede8de7/8f0ede0735fae6cdafb377ef0ab30f2443a70fda.jpg" pic_ext="jpeg" changedsize="true" width="560" height="497">
p = r'<img class="BDE_Image".*?src="([^"]*\.jpg)".*?>'
img_list = re.findall(p, html)
print()
try:
	os.mkdir('cat')
except FileExistsError:
	pass

os.chdir('cat')
for img in img_list:
	filename = img.split("/")[-1]
	request.urlretrieve(img, filename, cbk)






