# -*- coding:UTF-8 -*-
from bs4 import BeautifulSoup
import requests, sys
import urllib3
from requests_toolbelt import SSLAdapter

adapter = SSLAdapter('TLSv1')
s = requests.Session()
s.mount('https://', adapter)
urllib3.disable_warnings()



"""
类说明： 下载<<笔趣看>> 小说 邪气高手

"""

class downloader(object):

    def __init__(self):
        self.server = 'http://www.biqukan.com'
        self.target = 'http://www.biqukan.com/75_75364/'
        self.names = []   # 存放章节名
        self.urls = []
        self.nums = 0
    def get_download_url(self):
        req = requests.get(url = self.target)
        req.encoding = 'GBK'
        html = req.text
        div_bf = BeautifulSoup(html, 'lxml')
        div = div_bf.find_all('div', class_ = 'listmain')
        a_bf = BeautifulSoup(str(div[0]), 'lxml')
        a = a_bf.find_all('a')
        self.nums = len(a[12:])
        for each in a[12:]:
            self.names.append(each.string)
            # print(each.string)
            self.urls.append(self.server + each.get('href'))

    def get_contents(self, target):
        req = requests.get(url = target)
        req.encoding = 'GBK'
        html = req.text
        bf = BeautifulSoup(html, 'lxml')
        texts = bf.find_all('div', class_ = 'showtxt')
        texts = texts[0].text.replace('lxa0'*8, '\n\n')
        return texts
    
    def writer(self, name, path, text):
        write_flag = True
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')
    
if __name__ == '__main__':
    dl = downloader()
    dl.get_download_url()
    print("Let's begin")
    for i in range(dl.nums):
        dl.writer(dl.names[i], '邪x气高手.txt', dl.get_contents(dl.urls[i]))
        sys.stdout.write("  已下载:%.3f%%" %  float((i+1)/dl.nums*100) + '\r')
        sys.stdout.flush()
    print('endl')