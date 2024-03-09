import pyscreeze
import numpy as np
import pytesseract
import cv2
import difflib
import pyautogui
import time


def get_text_result():
    try:
        image = capture_text_result()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        # h, w = image.shape[:2]
        # gray = cv2.resize(gray, (w * 2, h * 2))
        _, binary_image = cv2.threshold(
            gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
        )

        cv2.imshow("screenshot", gray)
        cv2.waitKey(0)
        pytesseract.pytesseract.tesseract_cmd = r"./libs/Tesseract-OCR/tesseract.exe"
        config = r"--oem 3 --psm 6"
        txt_result = pytesseract.image_to_string(gray, config=config)
        # txt_result = pytesseract.image_to_string(gray)
        return txt_result
    except Exception as E:
        print(E)


def capture_text_result():
    # L362, T314, R817, B475
    left = 362
    top = 314
    right = 817
    bottom = 475
    screenshot = pyscreeze.screenshot(region=(left, top, right - left, bottom - top))
    screenshot = np.array(screenshot)
    return screenshot


# txt = get_text_result()
# print("text :", txt)


def compare_str():
    str1 = "Please scan lot no"
    str2 = "4l3a3e 5can lot"
    str3 = "scan lot no"

    percent_matching = round(difflib.SequenceMatcher(None, str1, str3).ratio() * 100, 2)
    print(f"{percent_matching}%")


# compare_str()

image = cv2.imread("./pass.png")


def capture_screenshot(left, top, width, height):

    screenshot = pyscreeze.screenshot(region=(left, top, width, height))
    screenshot = np.array(screenshot)
    return screenshot


def compare_image():
    # L229, T44, R826, B493 -> group box

    left = 229
    top = 44
    right = 826
    bottom = 493

    # left = 362
    # top = 314
    # right = 817
    # bottom = 475
    time.sleep(3)

    try:
        location = pyscreeze.locateOnScreen(
            image,
            minSearchTime=0.1,
            confidence=0.6,
            # region=(left, top, right - left, bottom - top),
            region=None,
            grayscale=True,
        )

        if location is not None:
            screenshot = capture_screenshot(
                int(location.left),
                int(location.top),
                int(location.width),
                int(location.height),
            )
            cv2.imshow("screenshot", screenshot)
            cv2.waitKey(0)
        else:
            print("Image not found on the screen.")
    except Exception as E:
        print(E)


compare_image()
