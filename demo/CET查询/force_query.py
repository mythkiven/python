# coding: utf-8
"""
暴力查询模块
1. 根据输入的前10为准考证号，暴力破解后5为准考证号（考场号3位 + 座位号2位）
2. 指定准考证号ID获取指定验证码图片
3. 图片输入机器学习模块，获取验证码值
4. 提交验证码进行查询，获取相应的结果：验证码错误/无结果/非上述两者，查询成功


准考证号列表

a. 获取验证码
b. 提交查询请求
    如果成功：结束
    如果验证码错误：重新获取验证码并提交
    如果查询结果为空：生成新的准考证号并提交

"""
import requests
from PIL import Image
from io import BytesIO
from get_images import get_image_url_and_filename
from settings import image_api, query_api, img_api_headers, query_api_headers
from validate_api import get_validate_code_from_image

myid = "你的准考证号前10位{id:05d}"
name = "你的姓名"


def log_info(*args):
    print("日志：", *args)


def send_query_until_true(num):
    # 生成准考证号
    new_id = myid.format(id=num)
    # 获取验证码图片地址
    img_api_url = image_api.format(id=new_id)
    img_api_resp = requests.get(img_api_url, headers=img_api_headers)
    img_url, filename = get_image_url_and_filename(img_api_resp.text)
    # 获取验证码图片并猜测
    img_resp = requests.get(img_url)
    code = get_validate_code_from_image(Image.open(BytesIO(img_resp.content)))
    # 执行查询操作
    data = {
        "data": "CET6_171_DANGCI,{id},{name}".format(id=new_id, name=name),
        "v": code
    }
    log_info(data)
    query_resp = requests.post(query_api, data=data, headers=query_api_headers)
    query_text = query_resp.text
    log_info(query_text)

    if "验证码错误" in query_text:
        query_text = send_query_until_true(num)
    return query_text


def main():
    for num in range(1, 10001):
        query_text = send_query_until_true(num)

        if "您查询的结果为空" in query_text:
            continue
        else:
            print("后五位是：", num)
            break


if __name__ == '__main__':
    main()
