# coding: utf-8
"""
统计标记的图片字母数字分布频数
"""

import os
import pprint


def get_filename_list():
    name = os.listdir("labeled_images")
    return name


def main():
    count_dct = {}
    name_list = get_filename_list()
    for name in name_list:
        for word in name[0:3]:
            if word not in count_dct:
                count_dct[word] = 1
            else:
                count_dct[word] += 1

    print("总计字符：", len(count_dct))
    pprint.pprint(count_dct)


if __name__ == '__main__':
    main()
