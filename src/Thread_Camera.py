from libs.libs import QThread, pyqtSignal, cv2, np
from src.utilities import config, logger, time


#! Camera Class


class CameraThread(QThread):
    frame_received = pyqtSignal(np.ndarray)
    update_error_signal = pyqtSignal()

    def __init__(self, camera_id, ref=None):

        super(CameraThread, self).__init__()
        self.camera_id = camera_id
        self.is_running = True
        self.cap = cv2.VideoCapture(self.camera_id, cv2.CAP_DSHOW)
        self.main_ref = ref
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1281)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1025)

    def run(self):
        is_alert_error = False
        while self.is_running:
            self.ret, self.frame = self.cap.read()
            if not self.ret:
                if not is_alert_error:
                    is_alert_error = True
                    self.update_error_signal.emit()
                    self.cap.release()
                    logger.error("Camera Error")
                    self.is_running = False
            else:
                is_alert_error = False
                self.frame_received.emit(self.frame)
            cv2.waitKey(1)
        # while self.is_running:
        #     try:
        #         self.ret, self.frame = self.cap.read()
        #         if self.ret:
        #             self.frame_received.emit(self.frame)
        #         else:
        #             # self.frame_received.emit(self.frame)
        #             self.update_error_signal.emit()
        #             # self.main_ref.set_error_camera_state(self)

        #     except Exception as E:
        #         self.cap.release()
        #         time.sleep(1)
        #         self.cap.open(self.camera_id, cv2.CAP_DSHOW)
        #         self.update_error_signal.emit()

    def stop(self):
        self.is_running = False
        self.requestInterruption()
        self.cap.release()
        self.quit()
