# coding: utf-8
"""
1. 切割标记好的图片
2. 将切割的图片分类保存至指定文件夹
"""

import os
from PIL import Image
from utils import do_image_crop

classify_dir = "predict_images"


def classify_croped_image_to_folder(img_list, img_name):
    """通过文件名将块图片存储至指定文件夹"""
    for n, word in enumerate(img_name[:4]):
        file_dir = os.path.join(classify_dir, word)
        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        img_list[n].save(os.path.join(classify_dir, word, img_name))


def main():
    name_list = os.listdir(classify_dir)
    for name in name_list:
        if not name.endswith(".png"):
            continue
        img = Image.open(os.path.join(classify_dir, name))
        piece_img_list = do_image_crop(img.copy())
        classify_croped_image_to_folder(piece_img_list, name)


if __name__ == '__main__':
    main()
