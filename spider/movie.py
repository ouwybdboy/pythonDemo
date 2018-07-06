# _*_ coding:utf-8 _*_

import requests
import re
from bs4 import BeautifulSoup
import sys

buffer = """
  __  __            _         _____       _     _
 |  \/  |          (_)       / ____|     (_)   | |
 | \  / | _____   ___  ___  | (___  _ __  _  __| | ___ _ __
 | |\/| |/ _ \ \ / / |/ _ \  \___ \| '_ \| |/ _` |/ _ \ '__|
 | |  | | (_) \ V /| |  __/  ____) | |_) | | (_| |  __/ |
 |_|  |_|\___/ \_/ |_|\___| |_____/| .__/|_|\__,_|\___|_|
                                   | |
                                   |_|
"""


class MovieSpider(object):
    '''Based paofan'''

    def __init__(self):
        self.urls = {}  # 保存匹配到的电影及名称
        self.names = []
        self.links = []
        self.host = "http://www.chapaofan.com/"
        self.serach_key = "http://www.chapaofan.com/search/"

    # 负责获取html页面
    def get_html(self, url):
        header = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":
            "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding":
            "gzip, deflate",
        }
        self.html = requests.get(url, headers=header).text

    # 负责获得搜索结果
    def get_urls(self):
        # 负责清理搜索结果
        def cleaning_data(data_li):
            re_href = r"""http://www.chapaofan.com/[0-9]{1,10}.html"""
            re_title = r"title=\".*\""
            for data in data_li:
                href = re.search(re_href, data).group(0)
                title = re.search(re_title, data).group(0).replace("title=", "")
                self.urls[title] = href

        re_rule = r"""<li style="width: 30%"><a href="http://www.chapaofan.com/[0-9]{1,20}.html" title=".*">.*</a>"""
        patern = re.compile(re_rule)
        urls = patern.findall(self.html)
        cleaning_data(urls)

    # 负责储存数据
    def save(self, data):
        file = open("test", "w", encoding="utf-8")
        file.write(data)
        file.close()

    # 判断是否退出
    def quite(self, choice):
        if choice.isalpha():
            if choice == "q":
                sys.exit(0)
        return choice

    # 负责取得下载地址
    def get_download(self, url):
        self.get_html(url)
        soup = BeautifulSoup(self.html, "lxml")
        download_urls = soup.select(".download-list > ul > li > a")
        for link in download_urls:
            print(link.text.replace(" ", ""), link['href'])

    # 输出
    def Printf(self, data_li, perfix="", fill_str="-", fill_num=30):
        count = 1
        print("\n" + fill_str * fill_num)
        for data in data_li:
            print("[%d]" % count + perfix + data)
            self.links.append(self.urls[data])
            count += 1
        print("\n" + fill_str * fill_num)

    # 主循环
    def main_loop(self):
        print(buffer)
        print("\t\t输入q退出")
        while True:
            movie_name = self.quite(input("[+]Movie Name >> "))
            self.get_html(self.serach_key + movie_name)
            self.get_urls()
            self.Printf(self.urls.keys(), "电影名称：")
            choice = self.links[int(self.quite(input("[+]请选择 : >> "))) - 1]
            self.quite(choice)
            self.get_download(choice)


def main():
    spider = MovieSpider()
    spider.main_loop()


if __name__ == '__main__':
    main()
