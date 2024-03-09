import pyscreeze
import numpy as np
import pytesseract
import cv2
import time


# def detect_label(screenshot):
#     pytesseract.pytesseract.tesseract_cmd = (
#         r"C:\Program Files\Tesseract-OCR\tesseract.exe"
#     )
#     # config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ</"
#     # config = r"--oem 3 --psm 6"
#     config = "--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789</"
#     try:
#         str_label = pytesseract.image_to_string(screenshot, config=config)
#         txt_result = str_label.strip().split(" ")[-1]
#         return txt_result
#     except Exception as E:
#         print(E)


def get_text_result():
    try:
        image = capture_text_result()
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        _, binary = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        cv2.imshow("screenshot", gray)
        cv2.waitKey(0)
        pytesseract.pytesseract.tesseract_cmd = r"./libs/Tesseract-OCR/tesseract.exe"
        # config = r"--oem 3 --psm 6"
        # txt_result = pytesseract.image_to_string(image, config=config)
        txt_result = pytesseract.image_to_string(gray)
        print("txt detected: ", txt_result)
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

    # screenshot = cv2.imread("./tat.png")
    return screenshot


scan_lot_no_temp = cv2.imread("./temp/pass_1.png")
pass_temp = cv2.imread("./temp/pass_2.png")
repetitive_operation_temp = cv2.imread("./repetitive_operation.png")


def capture_result_groupbox(left, top, width, height):
    capture_screen = pyscreeze.screenshot(region=(left, top, width, height))
    capture_screen = np.array(capture_screen)
    return capture_screen


def find_position_of_template(option):
    # time.sleep(3)
    # left = 229
    # top = 44
    # right = 826
    # bottom = 493
    if option == 0:
        template_image = scan_lot_no_temp
    elif option == 1:
        template_image = pass_temp

    try:
        location = pyscreeze.locateOnScreen(
            image=template_image,
            minSearchTime=0.1,
            confidence=0.9,
            # region=(left, top, right - left, bottom - top),
            region=None,
            grayscale=True,
        )

        if location is not None:
            screenshot = capture_result_groupbox(
                int(location.left),
                int(location.top),
                int(location.width),
                int(location.height),
            )
            # cv2.imshow(f"screenshot {option}", screenshot)
            # cv2.waitKey(0)
            cv2.imwrite(f"./temp/screenshot_{option}.png", screenshot)
            return True
        else:
            return False
    except Exception as E:
        print(E)
        return False


# is_matching = find_position_of_template(1)
# print(is_matching)
