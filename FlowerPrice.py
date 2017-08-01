import requests
import re
from bs4 import BeautifulSoup as bs
import pandas as pd

for pagenum in range(33,497):
    #pagenum = 33
    pageurl = 'http://www.dfetc.com/view/front.article.articleView/'+str(pagenum)+'/28/495.html'
    page = requests.get(pageurl).text
    #soup = bs(page, 'lxml').table
    flowerPatter = re.compile('水晶草')
    match = flowerPatter.search(page)
    #data = pd.read_html(page, match='满天星')
    if match:
        title = re.findall(r'<div class="articleTitle">(.*?)</div>',page)[0]
        print(title)
        print(pagenum)