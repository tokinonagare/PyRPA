import easyocr
import time
import os
import pyautogui
import cv2


def get_by_coordinate(x_start, x_end, y_start, y_end):
    """
    需要游戏窗口大小为1550*800
    :param x_start:
    :param x_end:
    :param y_start:
    :param y_end:
    :return:
    """
    reader = easyocr.Reader(['ch_sim', 'en'])
    if os.path.exists('Screenshot') is not True:
        os.mkdir('Screenshot')
    screen_shot_img_path = 'Screenshot/Shot_' + f'{time.strftime("%m%d%H%M%S")}.png'
    pyautogui.screenshot().save(screen_shot_img_path)

    img = cv2.imread(screen_shot_img_path)
    cropped = img[y_start:y_end, x_start:x_end]  # 裁剪坐标为[y0:y1, x0:x1]

    cv2.imwrite(screen_shot_img_path, cropped)

    result = reader.readtext(screen_shot_img_path, detail=0)
    if len(result) > 0:
        return result[0]
    else:
        return 0
