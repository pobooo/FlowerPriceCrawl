import requests
import re
import os
from bs4 import BeautifulSoup as bs
def record_state(state):
    t1 = open('state.txt', 'w', encoding='utf-8')
    t1.write(str(state))
    t1.close()
def check_state():
    f = open('state.txt')
    a = f.readlines()[0]
    f.close()
    return a
#dataAll = []
def get24huaprice():
    t = open('24hua上海仓现货促销.txt', 'a', encoding='utf-8')
    if check_state() == '0':
        data = '中文名称,' + '英文名称,'+ '颜色,'+'规格,'+'级别,'+'重量,'+'产地,'+'包装,'+'预定售价'
        t.write(data + '\n')
    s = requests.Session()  # 可以在多次访问中保留cookie
    login_url = 'http://www.24hua.cn/shop/user.php?act=signin'
    s.post(login_url, {'act':'loginok','username':'用户名', 'password': '密码', 'remember': '1'})  # POST帐号和密码，设置headers
    for id in range(int(check_state())+1,8236):#8222
        page = s.get('http://www.24hua.cn/shop/goods.php?id='+ str(id))  # 已经是登录状态了
        page = page.text.encode(page.encoding).decode('utf-8')
        flowerPatter = re.compile('data wrong！')
        match1 = flowerPatter.search(page)
        flowerPatter = re.compile('商品不存在')
        match2 = flowerPatter.search(page)
        if match1 or match2:
            continue
        chinese_name = re.findall(r'中文名称:(.*?)</div>',page)[0]
        chinese_name.replace(' ','')
        en_name = re.findall(r'英文名称:(.*?)</div>',page)
        if len(en_name) == 0 or en_name == ' ':
            en_name = '无信息'
        else:
            en_name = en_name[0]
        color = re.findall(r'颜色:(.*?)</div>',page)
        if len(color) == 0 or color == ' ':
            color = '无信息'
        else:
            color = color[0]
        gui_ge = re.findall(r'规格:(.*?)</div>', page)
        if len(gui_ge) == 0 or gui_ge == ' ':
            gui_ge = '无信息'
        else:
            gui_ge = gui_ge[0]
        level = re.findall(r'级别:(.*?)</div>', page)
        if len(level) == 0 or level == ' ':
            level = '无信息'
        else:
            level = level[0]
        weight = re.findall(r'重量:(.*?)</div>', page)
        if len(weight) == 0 or weight == ' ':
            weight = '无信息'
        else:
            weight = weight[0]
        oringin = re.findall(r'产地:(.*?)</div>', page)
        if len(oringin) == 0 or oringin == ' ':
            oringin = '无信息'
        else:
            oringin = oringin[0]
        package = re.findall(r'包装:(.*?)</div>', page)
        if len(package) == 0 or package == ' ':
            package = '无信息'
        else:
            package = package[0]
        price = re.findall(r'售价:(.*?)</div>', page)
        if len(price) == 0 or package == ' ':
            price = '无信息'
        else:
            price = price[0]
        data = chinese_name + ',' + en_name + ',' + color + ',' + gui_ge + ',' + level + ',' + weight + ',' + oringin + ',' + package + ',' + price +'\n'
        #dataAll.append(data)
        print(id)
        record_state(id)
        t.write(data)

if __name__ == "__main__":
    get24huaprice()