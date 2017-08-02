import requests
import re
import os
from bs4 import BeautifulSoup as bs
class Found(Exception):
    pass

def getFlowerPrice(id,name):
    Tall = []
    Aall = []
    Ball = []
    Call = []
    try:
        for year in [2015,2016,2017]:
            for month in ['01','02','03','04','05','06','07','08','09','10','11','12']:
                if year == 2017 and month == '08':
                    raise Found
                #year=2017
                #month='01'
                url = 'http://www.wmxhpf.com/cg.jsp?state=3&id='+id+'&t='+str(year)+str(month)
                page = requests.get(url).text
                flowerPatter = re.compile('对不起，没有找到你查询的信息')
                match = flowerPatter.search(page)
                if match:
                    continue
                #soup = bs(requests.get(url).text, 'lxml')
                #content = soup.find_all(attrs={"type":"text/javascript"})[2]
                time = re.findall(r'var tl = \[(.*?)\]',page)[0]
                time = time.replace('\'','')
                Alevel = re.findall(r'var a1 = \[(.*?)\]',page)[0]
                Blevel = re.findall(r'var a2 = \[(.*?)\]',page)[0]
                Clevel = re.findall(r'var a3 = \[(.*?)\]',page)[0]
                time = time.split(", ")
                Alevel = Alevel.split(", ")
                Blevel = Blevel.split(", ")
                Clevel = Clevel.split(", ")
                t = []
                A = []
                B = []
                C = []
                for i in range(0,len(time)):
                    if not str(year)+'/'+time[i] in t:
                        t.append(str(year)+'/'+time[i])
                        A.append(Alevel[i])
                        B.append(Blevel[i])
                        C.append(Clevel[i])
                Tall.extend(t)
                Aall.extend(A)
                Ball.extend(B)
                Call.extend(C)
    except Found:
        filename = name
        with open(filename, 'w', encoding='utf-8') as t:
            for i in range(0,len(Tall)):
                dataABC = Tall[i]+','+Aall[i]+','+Ball[i]+','+Call[i]
                t.write(dataABC + '\n')

def getall():
    url = 'http://www.wmxhpf.com'
    mainpage = requests.get(url).text
    soup = bs(mainpage, 'xml')
    list = soup.find_all('tr',class_="")
    print(len(list))
    for tr in list:
        td = tr.find_all('td')
        Name = td[0].a.string +'('+ td[2].string+')'+'('+ td[3].string+')'+'.txt'
        Name = Name.replace('/','-')
        Id = re.findall(r'\d+',td[0].a['href'])
        if os.path.exists(Name):
            continue
        getFlowerPrice(Id[0], Name)
        print(Name)

if __name__ == "__main__":
    getall()