import requests
import pprint

if __name__ == "__main__":
    baseUrl = "https://video.twimg.com//amplify_video/1749658834992566272/pl/avc1/720x1280/mp4a/128000/aXyqmjiZSg3Ec1mS.m3u8?container=cmaf"
    session = requests.session()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Referer": "https://twitter.com/lianmeng798/status/1770089256867844204"
    }
    content = requests.get(baseUrl, headers=headers).content.decode()
    print(content)