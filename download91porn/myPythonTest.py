import os
import re
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

isOK = True
threads = 5


def mainvideo(url, session):
    global isOK, threads
    videomain = session.get(url).content
    html = etree.HTML(videomain)
    if len(html.xpath('//video[@id="video-play"]/@data-src')) < 1:
        print("can't find data-source")
        return
    m3u8url = html.xpath('//video[@id="video-play"]/@data-src')[0]
    print(m3u8url)
    name = html.xpath('//h4[@class="container-title py-3 mb-0"]/text()')[0]
    name = re.sub("r[\"/?&\\\\:<>%'$#@^|]", '', name)
    # 如果下载的是MP4文件的话
    mp4list = os.listdir(os.getcwd())
    if '{}.mp4' in mp4list:
        print('{}.mp4这个文件已经存在，开始下一个项目……')
        return
    if 'mp4' in m3u8url:
        print('down load mp4 type file')
        tsbi = session.get(url).content
        with open('{}.mp4'.format(name), 'ab+') as f:
            f.write(tsbi)
        return
    # 如果不是，则继续下载m3u8文件
    baseurl = os.path.dirname(m3u8url.split('.m3u8')[0]) + '/'
    if 'https:' not in m3u8url:
        m3u8url = 'https:'+m3u8url
    m3u8 = session.get(m3u8url).content.decode('utf8')
    m3u8ts = re.sub('#E.*', '', m3u8)
    m3u8ts = [i for i in m3u8ts.split('\n') if len(i) > 1]
    print(m3u8ts)
    print('文件共有{}个分段'.format(len(m3u8ts)))
    pool = ThreadPoolExecutor(max_workers=threads)
    mp4 = {}
    fail = {}
    for index, i in enumerate(m3u8ts):
        t = pool.submit(dowload, index, i, baseurl, mp4, fail, session)

    pool.shutdown()
    while not isOK:
        for i in fail.keys():
            downloadTwice(i, m3u8ts[i], baseurl, mp4, fail, session)

    if os.path.isfile('{}.mp4'.format(name)):
        os.remove('{}.mp4'.format(name))
    for i in range(len(m3u8ts)):
        with open('{}.mp4'.format(name), 'ab+') as f:
            try:
                f.write(mp4[i])
            except Exception as e:
                print(e)

def downloadTwice(q, ts, baseurl, mp4, fail, session):
    global isOK
    try:
        if fail[q] == None:
            return
        url = baseurl + ts
        tsbi = session.get(url)
        assert tsbi.status_code == 200
        tsbi = tsbi.content
        mp4[q] = tsbi
        fail[q] = None
        print(q)
        isOK = True
    except AssertionError:
        isOK = False
        print('503:erro')
        pass
    except Exception as e:
        isOK = False
        print(e)
        pass

def dowload(q, ts, baseurl, mp4, fail, session):
    global isOK
    try:
        url = baseurl + ts
        tsbi = session.get(url)
        assert tsbi.status_code == 200
        tsbi = tsbi.content
        mp4[q] = tsbi
        print(q)
    except AssertionError:
        isOK = False
        fail[q] = ts
        print('503:erro:'+ str(url))
    except Exception as e:
        isOK = False
        fail[q] = ts
        print(str(e) + '\n' + str(url))

def main():
    global url
    session = requests.session()
    refer = url.split('/video')[0] + '/'
    session.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49',
        'referer': refer
    }
    main = session.get(url).content
    mainhtml = etree.HTML(main)
    find = mainhtml.xpath('//a[@class="display d-block" and @target="_self"]/@href')

    net = url.split('https://')[1].split('/')[0]
    print('{}个文件等待下载中……………… \n'.format(len(find)))
    print(find)
    for index, i in enumerate(find):
        print('执行进度{}%\n'.format(float(index) * 100.0 / float(len(find))))

        if 'https:' in i:
            print(i)
            mainvideo(i, session)
            url = i
        elif '//' in i:
            print('https:' + i)
            mainvideo('https:' + i, session)
            url = 'https:' + i
        else:
            print('https://' + net + i)
            mainvideo('https://' + net + i, session)
            url = 'https://' + net + i


if __name__ == '__main__':
    print('输入url先')
    url = str(input())
    print('最大线程数')
    threads = int(input())
    print('下载一页还是下载一个？Y/N')
    choice = input()
    print('是否开启无限循环？Y/N')
    loop = str(input())
    defaulurl = 'https://c7q06o.avlulu574.xyz/video/view/b3bc204e2331b2279b50'
    if url == '':
        url = defaulurl
    if choice == 'Y':
        if loop =='Y':
            while True:
                main()
        else:
            main()

    elif choice == 'N':
        session = requests.session()
        refer = url.split('/video')[0] + '/'
        session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.49',
            'referer': refer
        }
        mainvideo(url, session)

