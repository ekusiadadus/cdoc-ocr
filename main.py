import os
import numpy as np
import cv2
from PIL import Image
from google.cloud import vision
from google.cloud.vision_v1 import types
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

img = cv2.imread(str("test.png"))  # 画像の読み込み
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_byte = cv2.imencode('.png', img)[1].tobytes()

pdfmetrics.registerFont(TTFont('ipaexm', 'ipaexm.ttf'))  # 日本語フォントの登録

client = vision.ImageAnnotatorClient()


def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def get_word_info(response):  # google cloud visionから送られる結果の処理
    document = response.full_text_annotation
    bounds_word = []
    words = []
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_tmp = []
                    for symbol in word.symbols:
                        word_tmp.append(symbol.text)
                    bounds_word.append(word.bounding_box)
                    word_tmp = ''.join(word_tmp)
                    words.append(word_tmp)

    left_bottoms = []  # reportlabが左下を基準点として文字をレンダリングするため、左下の座標を保存しておく
    heights = []
    for bound in bounds_word:
        temp_xs = []
        temp_ys = []
        for vertice in bound.vertices:
            temp_xs.append(vertice.x)
            temp_ys.append(vertice.y)
        left_bottoms.append({'x': min(temp_xs), 'y': max(temp_ys)})
        heights.append(int(max(temp_ys) - min(temp_ys)))
    result = [{'text': text, 'box': bounds_word, 'vertic': vertic, 'height': height} for (
        text, bound, vertic, height) in zip(words, bounds_word, left_bottoms, heights)]

    return result


img_gcv = types.Image(content=img_byte)
response = client.document_text_detection(image=img_gcv)  # ocr実行！
results = get_word_info(response)  # 結果の処理

small_fix_y = 0.25  # reportlabのレンダリング時に下にずれるのを補正する

Y, X = img.shape[0], img.shape[1]
cc = canvas.Canvas("./output.pdf", pagesize=(X, Y))
cc.drawImage(ImageReader(cv2pil(img)), 0, 0, width=X, height=Y)
for result in results:
    cc.setFont('ipaexm', result['height']*0.9)
    cc.setFillColor(Color(0, 0, 0, alpha=0))  # 色は透明にする
    cc.drawString(result['vertic']['x'], Y - result['vertic']
                  ['y'] + small_fix_y*result['height'], result['text'])
cc.showPage()
cc.save()
