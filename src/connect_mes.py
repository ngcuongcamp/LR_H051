from libs.libs import Desktop, keyboard, pyautogui
from src.utilities import logger, cmd_printer
from src.UI_handler import set_error_mes_state


def get_name_mes_app(self):
    # print(self.MES_APP_NAME)
    top_windows = Desktop(backend=self.MES_BACKEND).windows()
    is_found = False
    for w in top_windows:
        if "login:" in w.window_text().lower() and "ver:" in w.window_text().lower():
            self.MES_APP_NAME = w.window_text()
            is_found = True
            break
    if is_found == False:
        set_error_mes_state(self)
        print("Can't connect with MES APP")
        logger.error("Can't connect with MES APP")


def send_data_to_mes(self, data: str):
    # L352, T104, R780, B136
    x = (780 - 352) / 2
    y = (136 - 104) / 2

    cmd_printer("INFO", "Start send")
    if self.IS_USE_AUTOCLICK == 1:
        pyautogui.click(x=x, y=y)
        pyautogui.typewrite(data)

    elif self.IS_USE_AUTOCLICK == 0:
        # x = 1024 / 2
        # y = 768 / 2
        pyautogui.moveTo(x, y)
        pyautogui.typewrite(data)
        pyautogui.moveTo(x, y)

    keyboard.press_and_release("enter")
    cmd_printer("INFO", "End send")
