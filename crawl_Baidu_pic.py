import requests
from bs4 import BeautifulSoup
import urllib
import re
import os
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome'
                  '/70.0.3538.102 Safari/537.36'
}


url22 = 'https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1' \
          '&sf=1&fmq=&pv=&ic=0&nc=1&z=&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&ie=utf-8' \
          '&fm=index&pos=history&word=lol'
r = requests.get(url22, headers=headers)
pic_urls22 = re.findall('"objURL":"(.*?)",', r.text, re.S)


def getMoreURL(word):
    urls = []
    for x in range(0, 150, 30):
        try:
            url = 'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&fp=result' \
                '&queryWord=' + word + '&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&ic=0&word=' \
                + word + '&face=0&istype=2nc=1&pn=' + str(x) + '&rn=30'
            # print(url)
            urls.append(url)
            # print(urls)
        except Exception as e:
            print(e)
            print('Error: getMoreURL')
    return urls


def picURL(urls):
    total_urls = []
    try:
        for pic_url in urls:
            html = requests.get(pic_url, headers=headers)
            pic_urls = re.findall('"objURL":"(.*?)",', html.text, re.S)
            for x in pic_urls:
                y = x.replace('_z2C$q', ':')
                z = y.replace('_z&e3B', '.')
                t = z.replace('AzdH3F', '/')
                intab = 'abcdefghijklmnopqrstuvw1234567890'
                outtab = '0852vsnkheb963wtqplifcadgjmoru147'
                trantab = str.maketrans(intab, outtab)
                jpg = t.translate(trantab)
                total_urls.append(jpg)
    except Exception as e:
        print(e)
        print('Error: picURL')
    return total_urls


def main():
    word = input('word: ')
    MoreURL = getMoreURL(word)
    total_urls = picURL(MoreURL)
    print(total_urls)
    down_pic(total_urls, word)


def down_pic(total_urls, word):
    path = 'd://pic/' + word + '/'
    if os.path.exists(path):
        pass
    else:
        os.mkdir(path)
    n = 0
    for i in total_urls:
        page = requests.get(i, headers=headers)
        with open(path + '00' + str(n) + '.jpg', 'wb') as f:
            f.write(page.content)
            n = n + 1
    print('共 %d 张图片' % n)


if __name__ == '__main__':
    main()
