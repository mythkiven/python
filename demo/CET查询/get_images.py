# coding: utf-8
import re
import requests

from settings import img_api_headers, image_api


def get_random_id():
    """获取随机的准考证号"""
    return "360450171200100"


def get_image_url_and_filename(text):
    """获取api返回的图片地址"""
    url = re.findall(r"imgs\(\"(.*?)\"\)", text)
    name = re.findall(r"imgs/(.*?\.png)", text)
    if url:
        r = url[0]
    else:
        raise ValueError
    return r, name[0]


def save_url_image_to_file(url, filename):
    """请求图片url，并保存至指定文件"""
    r = requests.get(url)
    with open("images/" + filename, "wb") as f:
        f.write(r.content)


def main():
    for i in range(200):
        ik = get_random_id()
        u = image_api.format(id=ik)
        r = requests.get(u, headers=img_api_headers)
        url, filename = get_image_url_and_filename(r.text)
        save_url_image_to_file(url, filename)


if __name__ == '__main__':
    main()
