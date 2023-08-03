import requests
import pprint
from Crypto.Cipher import AES
if __name__ == "__main__":
    baseUrl = r"https://sf07.aztc11.cn/video/2023-06-14/15/1668883146995150848/"
    url = r"https://sf07.aztc11.cn/video/2023-06-14/15/1668883146995150848/3559ddad496443929e6514135409b4d3.m3u8"
    session = requests.session()

    session.headers = {
        r"Referer": r"https://cgg01.com/?channelId=2",
        r"User-Agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183",
    }
    content = session.get(url).content.decode()
    key_url =