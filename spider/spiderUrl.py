'''
参考网络资源地址
https://www.toutiao.com/i6543111579162903053/?tt_from=weixin&utm_campaign=client_share&from=singlemessage&timestamp=1523499165&app=news_article&utm_source=weixin&isappinstalled=0&iid=30195832091&utm_medium=toutiao_ios&wxshare_count=2&pbid=6543379310681589261
'''
import os
import requests
from lxml import html
import time
from selenium import webdriver
etree = html.etree

# 将Chrome设置成不加载图片的无界面运行状态
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument("--headless")
# chromedriver与chrome版本映射表  https://blog.csdn.net/huilan_same/article/details/51896672
#将 chromedriver.exe 放到python安装路径下
# 修改为自己的实际路径
# chrome_path = 'D:\install\python3\chromedriver.exe'
chrome_path = 'D:\chromedriver.exe'
os.environ["webriver.chrome.driver"]=chrome_path
# 设置图片存储路径
PICTURES_PATH = os.path.join(os.getcwd(), 'pictures/')

# 设置headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Refere': "http://www.mmjpg.com/"
}


class Spider(object):
    def __init__(self, page_num):
        self.page_num = page_num
        self.page_urls = ['http://www.mmjpg.com/']
        self.girl_urls = []
        self.girl_name = ''
        self.pic_urls = []

    # 获取页面url的方法
    def get_page_urls(self):
        if int(page_num) > 1:
            for n in range(2, int(page_num) + 1):
                page_url = 'http://mmjpg.com/home/' + str(n)
                self.page_urls.append(page_url)
        elif int(page_num) == 1:
            pass

    # 获取妹子url的方法
    def get_girl_urls(self):
        for page_url in self.page_urls:
            html  = requests.get(page_url).content
            selector = etree.HTML(html)
            self.girl_urls += (selector.xpath('//span[@class="title"]/a/@href'))

    # 获取图片url的方法
    def get_pic_urls(self):
        driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
        for girl_url in self.girl_urls:
            driver.get(girl_url)
            time.sleep(4)
            driver.find_element_by_xpath('//em[@class="ch all"]').click()
            time.sleep(4)
            html = driver.page_source
            selector = etree.HTML(html)
            self.girl_name = selector.xpath('//div[@class="article"]/h2/text()')[0]
            self.pic_urls = selector.xpath('//div[@id="content"]/img/@data-img')
            try:
                self.download_pic()
            except Exception as e:
                print('{}保存失败'.format(self.girl_name) + str(e))

    # 下载图片的方法
    def download_pic(self):
        try:
            os.mkdir(PICTURES_PATH)
        except:
            pass
        girl_path = PICTURES_PATH + self.girl_name
        try:
            os.mkdir(girl_path)
        except Exception as e:
            print('{}已经存在'.format(self.girl_name))
        img_name = 0
        for pic_url in self.pic_urls:
            img_name += 1
            img_data = requests.get(pic_url, headers=headers)
            pic_path = girl_path + '/' + str(img_name) + '.jpg'
            if os.path.isfile(pic_path):
                print("{}第{}张已存在".format(self.girl_name, img_name))
                pass
            else:
                with open(pic_path, 'wb') as f:
                    f.write(img_data.content)
                    print("正在保存{}第{}张".format(self.girl_name, img_name))
        return

    # 爬虫的启动方法，按照爬虫逻辑依次调用方法
    def start(self):
        self.get_page_urls()
        self.get_girl_urls()
        self.get_pic_urls()


# main函数
if __name__ == '__main__':
    # page_num = input("请输入页码：")
    page_num = 2
    mmjpg_spider = Spider(page_num)
    mmjpg_spider.start()
