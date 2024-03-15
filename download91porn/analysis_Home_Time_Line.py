import json
'''

首先先打开x网站，找到充满视频的网页，然后点击F12，打开开发者模式
在network 输入timeline 然后将过滤出来的内容找到类似于Json格式的文件下载下来
然后将底下的JSONPATH改为下载下来的文件路径
就可以列出刚刚观看过的视频的视频url了

'''

JSONPATH = "C:/Users/Administrator/Desktop/Untitled-1.json"

# JSONPATH = "C:/Users/Administrator/Desktop/test.json"


def find_entries(dict):
    inst = None
    for k, v in dict.items():
        if k == "instructions":
            inst = v
        if inst:
            break
        for k1, v1 in v.items():
            if k1 == "instructions":
                inst = v1
            if inst:
                break
            for k2, v2 in v1.items():
                if k2 == "instructions":
                    inst = v2
                if inst:
                    break
    if inst:
        for i in inst:
            if i['type'] == "TimelineAddEntries":
                return i['entries']


if __name__ == "__main__":
    with open(JSONPATH, "r", encoding="UTF-8") as f:
        # file = f.read()
        js = json.load(f)

    entries = find_entries(js["data"])
    for i in entries:
        try:
            if i["content"].get("itemContent", None):
                name = i["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["full_text"]
                urls = i["content"]["itemContent"]["tweet_results"]["result"]["legacy"]["entities"]["media"]
            elif i["content"].get("items", None):
                name = i["content"]["items"][0]["item"]["itemContent"]["tweet_results"]["result"]["legacy"]["full_text"]
                urls = i["content"]["items"][0]["item"]["itemContent"]["tweet_results"]["result"]["legacy"]["entities"]["media"]
            # print(name)
            # print(urls)
            for media in urls:
                high = media["original_info"]["width"]
                vars = media["video_info"]["variants"]
                # print(high)
                # print(vars)
                high_url = ""
                m3u8_url = ""
                for var in vars:
                    if str(high) in var["url"]:
                        high_url = var["url"]
                    if "m3u8" in var["url"]:
                        m3u8_url = var["url"]
                print(f"name is {name} \nhigh url is {high_url} \nm3u8 url is {m3u8_url}")
                print("\n\n\n")
        except Exception as e:
            pass

