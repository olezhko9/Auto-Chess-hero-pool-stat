import pytesseract
import cv2
import numpy as np
from PIL import Image
from util.img_croper import crop_hero_text
from dac.hero_list import all_heroes

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def recognize_heroes_on_image(image, need_crop=False, show=False):

    if type(image) == str:
        image = Image.open(image)

    image = np.array(image)

    if need_crop:
        image = crop_hero_text(image)

    return recognize_heroes(image, show)


def recognize_heroes(image, show):
    # насыщенные буквы на черном фоне
    retval, saturated_image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)

    # переводим в оттенки серого
    grayscaled = cv2.cvtColor(saturated_image, cv2.COLOR_BGR2GRAY)

    # бинаризация изображения
    retval, bw_image = cv2.threshold(grayscaled, 20, 255, cv2.THRESH_BINARY)

    # черные буквы на белом фоне
    bw_image[bw_image == 255] = 100
    bw_image[bw_image == 0] = 255
    bw_image[bw_image == 100] = 0

    if show:
        cv2.imshow('threshold', bw_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return get_heroes_from_text(pytesseract.image_to_string(bw_image, lang='eng', config='--psm 7'))


def get_heroes_from_text(text):
    # TODO: Io распознается как lo - исправить
    hero_list = []
    for hero in all_heroes:
        hero_index = -1
        while True:
            hero_index = text.find(hero, hero_index + 1)
            if hero_index == -1:
                break
            else:
                hero_list.append((hero_index, hero))

    hero_list = [h[1] for h in sorted(hero_list, key=lambda x: x[0])]

    return hero_list
