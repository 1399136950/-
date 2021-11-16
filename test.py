from random import randint
import time

import cv2
from selenium import webdriver
import numpy as np

import win32api
import win32con


def mouse_hold_and_move(start_x, start_y, dst):
    """
    从起始坐标开始， 按住鼠标并横向移动
    @param start_x: 起始x坐标
    @param start_y: 起始y坐标
    @param dst: x轴移动距离大小
    @return:
    """
    win32api.SetCursorPos((start_x, start_y))   # 移动到指定坐标
    time.sleep(0.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 200, 200, 0, 0)  # 左键按下
    time.sleep(0.2)
    v0, t1, t2 = 300, 0.5, 0.2    # 初速度、加速时长和减速时长
    a1 = (dst - v0 * t1 - 0.5 * t2 * v0) / (0.5 * t1 * (t1 + t2))  # 加速度大小
    a2 = -1 * (v0 + a1 * t1) / t2   # 减速度大小
    sept = 0.01  # 时间间隔
    t, d = 0, 0  # 初始时刻和位移
    a1_mid = a1 * 0.5
    a2_mid = a2 * 0.5
    while t < t1:
        d = int(t * (v0 + a1_mid * t))
        t += sept
        win32api.SetCursorPos((start_x+d, start_y+randint(-4, 4)))
        time.sleep(sept)
    t = 0
    v0 = v0 + a1*t1
    while t < t2:
        d1 = int(t * (v0 + a2_mid * t))
        t += sept
        win32api.SetCursorPos((start_x + d + d1, start_y+randint(-4, 4)))
        time.sleep(sept)
    win32api.SetCursorPos((start_x + dst, start_y+randint(-4, 4)))
    time.sleep(0.5)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 200, 200, 0, 0)   # 左键松开


if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.get('url_address')
    driver.maximize_window()
    driver.implicitly_wait(3)
    input_ = driver.find_element_by_css_selector('input[class="el-input__inner"]')
    input_.send_keys('phone_number')  # 填写手机号
    target_image = cv2.imread('target.png')

    span = driver.find_element_by_css_selector('span[class="getCode"]')  # 点击获取验证码
    span.click()
    time.sleep(3)

    canvas = driver.find_element_by_css_selector('#slideVerify canvas')  # 滑动验证码画布

    img_bin = canvas.screenshot_as_png  # canvas截图

    background_image = np.array(bytearray(img_bin), dtype=np.uint8)
    background_image = cv2.imdecode(background_image,  cv2.IMREAD_COLOR)

    res = cv2.matchTemplate(background_image, target_image, cv2.TM_CCOEFF_NORMED)  # 模板匹配

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print(max_loc)
    all_dst = max_loc[0]
    mouse_hold_and_move(600, 650, int(all_dst/0.911))
    time.sleep(2)
