import requests
import pprint

if __name__ == "__main__":
    baseUrl = ""
    session = requests.session()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0",
        "Referer": "https://twitter.com/lianmeng798/status/1770089256867844204"
    }
    content = requests.get(baseUrl, headers=headers).content.decode()
    print(content)