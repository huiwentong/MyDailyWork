import re
import requests
import m3u8
import time
import os
from bs4 import BeautifulSoup
import json
from Crypto.Cipher import AES
import sys
import random
import uuid

class VideoCrawler():
    def __init__(self, url):
        super(VideoCrawler, self).__init__()
        self.url = url
        self.down_path = os.getcwd()+r'\Temp'
        self.agency_url = 'https://www.kuaidaili.com/free/'  # 获取免费代理的网站，如果网站过期或者失效，自己找代理网站替换
        self.final_path = os.getcwd()+r'\Final'
        self.headers = {
            'Connection': 'Keep-Alive',
            'Accept': 'text/html,application/xhtml+xml,*/*',
            'User-Agent': 'Mozilla/5.0 (Linux; U; Android 6.0; zh-CN; MZ-m2 note Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 MZBrowser/6.5.506 UWS/2.10.1.22 Mobile Safari/537.36'
        }

    def get_url_from_m3u8(self, readAdr):
        print("正在解析真实下载地址...")
        with open('temp.m3u8', 'wb') as file:
            file.write(requests.get(readAdr).content)
        m3u8Obj = m3u8.load('temp.m3u8')
        print("解析完成")
        return m3u8Obj.segments

    def get_ip_list(self, url, headers):
        web_data = requests.get(url, headers=headers).text
        soup = BeautifulSoup(web_data, 'lxml')
        ips = soup.find_all('tr')
        ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')
            ip_list.append(tds[0].text + ':' + tds[1].text)
        return ip_list

    def get_random_ip(self, ip_list):
        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        proxy_ip = random.choice(proxy_list)
        proxies = {'http': proxy_ip}
        return proxies

    def run(self):
        print("Start!")
        start_time = time.time()
        self.down_path = r"%s\%s" % (self.down_path, uuid.uuid1())  # 拼接新的下载地址
        if not os.path.exists(self.down_path):  # 判断文件是否存在，不存在则创建
            os.makedirs(self.down_path)
        html = requests.get(self.url).text
        bsObj = BeautifulSoup(html, 'lxml')
        tempStr = bsObj.find(class_="iplays").contents[3].string  # 通过class查找存放m3u8地址的组件
        firstM3u8Adr = json.loads(tempStr.strip('var player_data='))["url"]  # 得到第一层m3u8地址
        tempArr = firstM3u8Adr.rpartition('/')
        all_content = (requests.get(firstM3u8Adr).text).split('\n')[2]  # 从第一层m3u8文件中中找出第二层文件的的地址
        midStr = all_content.split('/')[0]  # 得到其中有用的字符串，这个针对不同的网站采用不同的方法自己寻找其中的规律
        realAdr = "%s/%s" % (tempArr[0], all_content)  # 一定规律下对字符串拼接得到第二层地址， 得到真实m3u8下载地址，
        key_url = "%s/%s/hls/key.key" % (tempArr[0], midStr)  # 分析规律对字符串拼接得到key的地址
        key_html = requests.head(key_url)  # 访问key的地址得到的文本
        status = key_html.status_code  # 是否成功访问到key的地址
        key = ""
        if status == 200:
            all_content = requests.get(realAdr).text  # 请求第二层m3u8文件地址得到内容
            if "#EXT-X-KEY" in all_content:
                key = requests.get(key_url).content  # 如果其中有"#EXT-X-KEY"这个字段说明视频被加密
        self.fileName = bsObj.find(class_="video-title w100").contents[0].contents[0]  # 分析网页得到视频的名称
        self.fileName = re.sub(r'[\s,!]', '', self.fileName)  # 因为如果文件名中有逗号感叹号或者空格会导致合并时出现命令不正确错误，所以通过正则表达式直接去掉名称中这些字符
        iv = b'abcdabcdabcdabcd'  # AES解密时候凑位数的iv
        if len(key):  # 如果key有值说明被加密
            cryptor = AES.new(key, AES.MODE_CBC, iv)  # 通过AES对ts进行解密
        urlList = self.get_url_from_m3u8(realAdr)
        urlRoot = tempArr[0]
        i = 1
        outputfile = open(os.path.join(self.final_path, '%s.ts' % self.fileName),
                          'wb')  # 初始创建一个ts文件，之后每次循环将ts片段的文件流写入此文件中从而不需要在去合并ts文件
        ip_list = self.get_ip_list(self.agency_url, self.headers)  # 通过网站爬取到免费的代理ip集合
        for url in urlList:
            try:
                proxies = self.get_random_ip(ip_list)  # 从ip集合中随机拿到一个作为此次访问的代理
                resp = requests.get("%s/%s/hls/%s" % (urlRoot, midStr, url.uri), headers=crawler.headers,
                                    proxies=proxies)  # 拼接地址去爬取数据，通过模拟header和使用代理解决封IP
                if len(key):
                    tempText = cryptor.decrypt(resp.content)  # 解密爬取到的内容
                    progess = i / len(urlList)  # 记录当前的爬取进度
                    outputfile.write(tempText)  # 将爬取到ts片段的文件流写入刚开始创建的ts文件中
                    sys.stdout.write('\r正在下载：%s,进度：%s %%' % (self.fileName, progess))  # 通过百分比显示下载进度
                    sys.stdout.flush()  # 通过此方法将上一行代码刷新，控制台只保留一行
                else:
                    outputfile.write(resp.content)
            except Exception as e:
                print("\n出现错误：%s", e.args)
                continue  # 出现错误跳出当前循环，继续下次循环
            i += 1
        outputfile.close()
        print("下载完成！总共耗时%d s" % (time.time() - start_time))
        self.del_tempfile()  # 删除临时文件

    def del_tempfile(self):
        file_list = os.listdir(self.down_path)
        for i in file_list:
            tempPath = os.path.join(self.down_path, i)
            os.remove(tempPath)
        os.rmdir(self.down_path)
        print('临时文件删除完成')


if __name__ == '__main__':
    url = input("输入地址：\n")
    crawler = VideoCrawler(url)
    crawler.run()
    quitClick = input("请按Enter键确认退出！")