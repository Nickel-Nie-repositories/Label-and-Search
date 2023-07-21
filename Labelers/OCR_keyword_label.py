import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from paddleocr import PaddleOCR

import jieba.analyse as ana

# # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
# # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
# ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
# img_path = r'D:\PythonProject\Label_and_Search\test.png'
# result = ocr.ocr(img_path, cls=True)
# for line in result:
#     print(line)

# # 显示结果
# from PIL import Image
#
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('Result.jpg')

ocr = PaddleOCR(use_angle_cls=True, lang="ch")


# 输入图片，输出图片上所有的文本的函数。
def OCR_label(image_path: str) -> str:
    result = ocr.ocr(image_path, cls=True)
    texts = [line[1][0] for line in result]
    text = "".join(texts)
    return text


def OCR_keywords_label(image_path: str) -> str:
    return " ".join(take_keywords(OCR_label(image_path)))


# 输入文本，输出若干个该文本中的关键词的函数。
def take_keywords(text: str) -> list[str]:
    # keyword = ana.textrank(text)
    keyword = ana.tfidf(text)
    return keyword


def test_label(image_path: str) -> str:
    return "_Label_"


if __name__ == "__main__":
    test_image = r'D:\PythonProject\Label_and_Search\test.png'
    r_text = OCR_label(test_image)
    # print(r_text)
    # print(take_keywords(r_text))
