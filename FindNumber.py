from ctypes import windll, byref, c_ubyte
from ctypes.wintypes import RECT, HWND
import numpy as np
import time
import os
import pyautogui


class FindNumber(object):
    def get_by_coordinate(self, x_start, x_end, y_start, y_end):
        """
        需要游戏窗口大小为1550*800
        :param x_start:
        :param x_end:
        :param y_start:
        :param y_end:
        :return:
        """
        if os.path.exists('Screenshot') is not True:
            os.mkdir('Screenshot')
        screen_shot_img_path = 'Screenshot/Shot_' + f'{time.strftime("%m%d%H%M%S")}.png'
        pyautogui.screenshot().save(screen_shot_img_path)
        import cv2

        img = cv2.imread(screen_shot_img_path)
        cropped = img[y_start:y_end, x_start:x_end]  # 裁剪坐标为[y0:y1, x0:x1]

        cv2.imwrite(screen_shot_img_path, cropped)
        numbers = self.make_number_list(screen_shot_img_path)
        return self.make_number(numbers)

    @staticmethod
    def make_number_list(img_path):
        import cv2
        # 加载数字模板
        temps = []
        for i in range(10):
            temps.append(cv2.imread(f'temple_numbers/{i}.png', cv2.IMREAD_GRAYSCALE))

        # 按下任意键退出识别
        # while cv2.waitKey(delay=100) == -1:
        im = cv2.imread(img_path)
        im_grayed = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        # im = im[157:655, 355:1148]
        # 提取指定画面中的数字轮廓
        gray = cv2.cvtColor(im, cv2.COLOR_BGRA2GRAY)
        # print('gray', gray)
        ret, thresh = cv2.threshold(im_grayed, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        contours = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
        result = []
        for cnt in contours:
            [x, y, w, h] = cv2.boundingRect(cnt)
            # 按照高度筛选
            if h == 11 and 8 >= w >= 7:
                result.append([x, y, w, h])

        result.sort(key=lambda x: x[0])
        print('寻找到的数字坐标：', result)
        numbers = []
        for x, y, w, h in result:
            # 在画面中标记识别的结果
            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 1)
            digit = cv2.resize(thresh[y:y + h, x:x + w], (14, 22))
            res = []
            for i, t in enumerate(temps):
                score = cv2.matchTemplate(digit, t, cv2.TM_CCORR_NORMED)
                res.append((i, score[0]))
            res.sort(key=lambda x: x[1])
            # print('res', res)
            # cv2.putText(im, str(f"{res[-1][0]}"), (x, y+35), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0))
            # cv2.imshow('Digits OCR Test', im)
            numbers.append(res[-1][0])
        print('识别到的数字：', numbers)
        return numbers

    @staticmethod
    def make_number(numbers):
        number_count = len(numbers)
        number = 0
        if number_count <= 0:
            print('没有找到数字！')
            return number

        first_number = numbers[0]
        if first_number == 0:
            for i in range(number_count):
                current_number = numbers[i]
                if current_number != 0:
                    number += numbers[i] / 10 ** i

            number = round(number, number_count - 1)
        else:
            for i in range(number_count):
                current_number = numbers[i]
                if current_number != 0:
                    number += numbers[i] * 10 ** (number_count - (i + 1))
        print('每个数字：', number)
        return number
