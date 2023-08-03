#!C:\Python3.7
# -*- coding:utf-8 -*-
# coding=utf-8
import requests
import os

headers = {
    "User - Agent": "Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 84.0.4147.105 Safari / 537.36"
}


def download(baseurl, file_m3u8, path_in):
    url_list = []
    with open(file_m3u8, "r") as f:
        for r in f.readlines():
            if ".ts" in r:
                url_list.append(r.replace("\n", "").strip())
    # print(url_list)

    for r in url_list:
        url = baseurl + r
        filename = os.path.join(path_in, r.split("_")[1])
        # print(url,filename)
        try:
            re = requests.get(url=url, headers=headers)
        except Exception as e:
            print(e)
            pass
        with open(filename, "ab") as f:
            f.write(re.content)
            print("[*]download:" + filename)


def mergeFileToMP4(pathname):
    os.chdir(pathname)
    cmd = "copy /b *.ts new.tmp"
    os.system(cmd)
    os.system('del /Q *.ts')
    os.system('del /Q *.mp4')
    os.rename("new.tmp", "new.mp4")
    os.chdir('..')
    print("merge file is :", str(os.path.join(pathname, "new.mp4")))


def key_test(key):
    print(len(key))
    key_hex = ""
    for c in key:
        tem = hex(ord(c))[2:]
        key_hex = key_hex + tem
    print(key_hex)
    return key_hex


def decode_openssl(key, iv, path_in, path_out):
    for file in os.listdir(path_in):
        file_in = os.path.join(path_in, file)
        file_out = os.path.join(path_out, file)
        # print(file_in,file_out)
        cmd = f"openssl aes-128-cbc -d -in {file_in} -out {file_out} -nosalt -iv {iv} -K {key}"
        print(cmd)
        os.system(cmd)


def clear_ts(path):
    os.chdir(path)
    os.system("del /Q *.ts")


def main(baseurl, key, iv, file_m3u8):
    # print("main")
    basepath = os.path.split(file_m3u8)[0]
    basepath_in = os.path.join(basepath, "in")
    basepath_out = os.path.join(basepath, "out")
    if not os.path.exists(basepath_in):
        os.mkdir(basepath_in)
    if not os.path.exists(basepath_out):
        os.mkdir(basepath_out)

    download(baseurl=baseurl, file_m3u8=file_m3u8, path_in=basepath_in)
    key = key_test(key)
    decode_openssl(key, iv, basepath_in, basepath_out)
    mergeFileToMP4(basepath_out)
    clear_ts(basepath_in)


if __name__ == '__main__':
    # https://xxxxxxx/video/20210713/ea044c31965940559162b816ec8e152a/cloudv-transfer/a08a0bff11c84000b465638605564520_0000001.ts
    baseurl = "https://xxxxxxxxx/video/20210713/ea044c31965940559162b816ec8e152a/cloudv-transfer/"
    key = "±úx£Ú:êh'ÿs{câ"
    iv = "131f71ed838a8019b731be5b7f2a1703"
    file_m3u8 = "./jixian/3.m3u8"
    file_m3u8 = os.path.join(os.getcwd(), file_m3u8)
    if (os.path.exists(file_m3u8)):
        main(baseurl, key, iv, file_m3u8)
    else:
        print("[-]" + file_m3u8 + " not found:\n")
    # download(baseurl)

