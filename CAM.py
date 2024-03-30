from libs.libs import *
from src.utilities import *
from src.Thread_PLC import PLCThread
from src.Thread_Camera import CameraThread
from src.connect_mes import *
from src.reader import *
from src.UI_handler import *
from src.detect_result import *


class MyApplication(QMainWindow):
    frame1 = None
    frame2 = None
    data_scan1 = None
    data_scan2 = None
    result_mes_operation = [False, False]
    graph = FilterGraph()
    thread_pool = QThreadPool()

    def __init__(self):
        super().__init__()
        self.is_update_cam_error = True
        self.is_processing = False
        self.state_ui = None

        initial_UI_MainWindow(self)  # initialize UI
        read_config(self)  # read config

        # thread CAMERA
        self.open_camera_thread()
        self.check_error_camera = QTimer()
        self.check_error_camera.timeout.connect(self.reconnect_camera_thread)
        self.check_error_camera.start(1000)

        # get_name_mes_app(self)  # connect MES APP

        # thread PLC
        self.THREAD_PLC = PLCThread(
            self.COM_PLC, self.BAUDRATE_PLC, timeout=0.009, ref=self
        )
        self.THREAD_PLC.start()
        self.THREAD_PLC.data_received.connect(self.handle_signal_plc)

    def handle_click_update(self, event):
        req = QMessageBox.question(
            self,
            "Confirm Update",
            "Do you want to update latest version?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )
        if req == QMessageBox.Yes:
            cmd_printer("WARNING", "Handler update function here...")

            req3 = QMessageBox.warning(
                self, "Information", "Not found latest version!", QMessageBox.Cancel
            )
        else:
            print("Ignore update")

    # handle plc signal
    def handle_signal_plc(self, data):
        if self.THREAD_CAMERA_1.is_running and self.THREAD_CAMERA_2.is_running:
            # if data == b"1":
            print("\n\n")
            print("------ SCAN SIGNAL -------")
            logger.info("\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
            logger.info("--> Received scan signal from PLC")
            logger.info("--> ------ SCAN SIGNAL -------")
            try:
                self.worker = Worker(self.scan_product_code)
                MyApplication.thread_pool.start(self.worker)
                # self.worker.autoDelete()
            except Exception as E:
                cmd_printer("ERROR", str(E))
        # if data == b"2":
        #     cmd_printer("WARNING", "---------------\nRESET")
        #     set_reset_state(self)
        #     self.state_ui = None
        #     self.set_default_variables()
        #     self.is_processing = False
        else:
            cmd_printer(
                "ERROR", "Error: Received signal when the camera is not connected"
            )
            cmd_printer("ERROR", f"Signal PLC: {data}")

    def scan_product_code(self):
        stime = time.time()
        # set_default_state(self)
        self.set_default_variables()
        i = 0
        while i < self.SCAN_LIMIT:
            i = i + 1
            frames = process_frame1(self, self.frame1)
            frames2 = process_frame2(self, self.frame2)
            self.data_scan1 = read_code_wechat(frames)
            self.data_scan2 = read_code_wechat(frames2)

            self.data_scan1 = "11111111111111111"
            self.data_scan2 = "22222222222222222"

            if self.data_scan1 is not None and self.data_scan2 is not None:
                break

        print("--> RESULT SCAN")
        logger.info("--> RESULT SCAN")
        print(f"-----> spends {round(time.time() - stime,3)}s to read code")

        # IF FAIL SCAN
        if self.data_scan1 is None or self.data_scan2 is None:
            cmd_printer("ERROR", "FAILED")
            logger.error("FAILED")
            self.THREAD_PLC.send_signal_to_plc(b"2")
            self.is_processing = False
            if self.IS_SAVE_NG_IMAGE == 1:
                if self.data_scan1 is None:
                    image_filename = "image_NG/{}/CAMERA1/{}.png".format(
                        get_current_date(), format_current_time()
                    )
                    cv2.imwrite(image_filename, self.frame1)
                if self.data_scan2 is None:
                    image_filename = "image_NG/{}/CAMERA2/{}.png".format(
                        get_current_date(), format_current_time()
                    )
                    cv2.imwrite(image_filename, self.frame2)

            logger.error("------FAIL SCAN-------")
            logger.error(f"Data SN: {self.data_scan1}")
            logger.error(f"Data FIXTURE: {self.data_scan2}")

            cmd_printer("ERROR", "------FAIL SCAN-------")
            print(f"Data SN: {self.data_scan1}")
            print(f"Data FIXTURE: {self.data_scan2}")
            if self.state_ui in [True, None]:
                set_fail_state(self)
                try:
                    self.update()
                    # self.repaint()
                except Exception as E:
                    print(E)
                # self.repaint()
                self.state_ui = False

        # IF PASS SCAN
        if self.data_scan1 is not None and self.data_scan2 is not None:
            is_matching_1 = None
            is_matching_2 = None
            cmd_printer("SUCCESS", "PASS SCAN")
            logger.info("PASS SCAN")
            print(f"Data SN: {self.data_scan1}")
            print(f"Data FIXTURE: {self.data_scan2}")

            print("----------- SEND TO MES -----------")
            logger.info("----------- SEND TO MES -----------")

            # reset result_mes_operation variable
            self.result_mes_operation = [False, False]

            # PUSH SN CODE
            send_data_to_mes(self, self.data_scan1)
            print(f"--> Send Data SN:  {self.data_scan1}")
            logger.info(f"--> Send Data SN:  {self.data_scan1}")
            time.sleep(self.TIME_SLEEP)

            stime = time.time()
            # 3 seconds to detect
            while self.WAIT_TIME > time.time() - stime:
                is_matching_1 = find_position_of_template(self, option=0)
                if is_matching_1 == True:
                    self.result_mes_operation[0] = True
                    logger.info("PASS TO CHECK SN CODE")
                    break

            # fail sn code
            if is_matching_1 == False:
                self.result_mes_operation[0] = False
                self.THREAD_PLC.send_signal_to_plc(b"2")
                self.is_processing = False
                cmd_printer("ERROR", "SIGNAL FAIL CHECK SN CODE FROM mes")
                if self.state_ui in [True, None]:
                    set_fail_state(self)
                    try:
                        self.update()
                        # self.repaint()
                    except Exception as E:
                        print(E)
                    # self.repaint()
                    self.state_ui = False

            # pass sn code -> send fixture code
            if self.result_mes_operation[0] == True:
                send_data_to_mes(self, self.data_scan2)
                print(f"--> Send Data FIXTURE:  {self.data_scan2}")
                logger.info(f"--> Send Data FIXTURE:  {self.data_scan2}")

                stime2 = time.time()

                while self.WAIT_TIME > time.time() - stime2:
                    is_matching_2 = find_position_of_template(self, option=1)
                    if is_matching_2 == True:
                        self.result_mes_operation[1] = True
                        logger.info("PASS TO CHECK FIXTURE CODE")
                        break

                if is_matching_2 == False:
                    self.result_mes_operation[0] = False
                    self.THREAD_PLC.send_signal_to_plc(b"2")
                    self.is_processing = False
                    self.is_processing = False
                    cmd_printer("ERROR", "SIGNAL FAIL CHECK FIXTURE CODE FROM mes")
                    if self.state_ui in [True, None]:
                        set_fail_state(self)
                        try:
                            self.update()
                            # self.repaint()
                        except Exception as E:
                            print(E)
                        self.state_ui = False

                if self.result_mes_operation == [True, True]:
                    cmd_printer("SUCCESS", "--> PASS MES")
                    logger.info("------PASS MES-------")
                    logger.info(f"Data SN: {self.data_scan1}")
                    logger.info(f"Data FIXTURE: {self.data_scan2}")
                    self.THREAD_PLC.send_signal_to_plc(b"1")
                    self.is_processing = False
                    if self.state_ui in [False, None]:
                        set_state_pass(self)
                        try:
                            self.update()
                            # self.repaint()
                        except Exception as E:
                            print(E)
                        self.state_ui = True
                    self.set_default_variables()

    def set_default_variables(self):
        self.data_scan1 = None
        self.data_scan2 = None
        self.result_mes_operation = [False, False]

    def display_frame1(self, frame):
        self.frame1 = frame
        # frame_zoom_out = cv2.resize(frame, (320, 240))
        frame_rgb = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)
        img = QImage(
            frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888
        )
        scaled_pixmap = img.scaled(self.Uic.CameraFrame1.size())
        pixmap = QPixmap.fromImage(scaled_pixmap)
        self.Uic.CameraFrame1.setPixmap(pixmap)

    def display_frame2(self, frame):
        self.frame2 = frame
        # frame_zoom_out = cv2.resize(frame, (320, 240))
        frame_rgb = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
        img = QImage(
            frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888
        )
        scaled_pixmap = img.scaled(self.Uic.CameraFrame2.size())
        pixmap = QPixmap.fromImage(scaled_pixmap)
        self.Uic.CameraFrame2.setPixmap(pixmap)

    def closeEvent(self, event):
        req = QMessageBox.question(
            self,
            "Confirm Close",
            "Do you want to close the application?",
            QMessageBox.Yes | QMessageBox.Cancel,
            QMessageBox.Cancel,
        )
        if req == QMessageBox.Yes:
            event.accept()
            self.THREAD_CAMERA_1.stop()
            self.THREAD_CAMERA_2.stop()
            self.THREAD_PLC.stop()
            cmd_printer("WARNING", "--------------\nCLOSE")

            # Close Camera and release
            if self.THREAD_CAMERA_1.isRunning():
                # self.THREAD_CAMERA_1.wait()
                self.THREAD_CAMERA_1.cap.release()
            if self.THREAD_CAMERA_2.isRunning():
                # self.THREAD_CAMERA_2.wait()
                self.THREAD_CAMERA_2.cap.release()
            cv2.destroyAllWindows()
        else:
            event.ignore()

    def update_status_camera_error(self):
        self.is_update_cam_error = True
        if self.is_update_cam_error:
            logger.error(f"CAM ERROR")
            self.is_update_cam_error = False
        set_error_camera_state(self)
        self.state_ui = None

    def open_camera_thread(self):
        # thread camera 1
        self.THREAD_CAMERA_1 = CameraThread(self.ID_C1)
        self.THREAD_CAMERA_1.frame_received.connect(self.display_frame1)
        self.THREAD_CAMERA_1.start()
        self.THREAD_CAMERA_1.cap.set(cv2.CAP_PROP_SATURATION, 0)
        self.THREAD_CAMERA_1.cap.set(cv2.CAP_PROP_EXPOSURE, self.PROP_EXPOSURE_1)
        if self.IS_OPEN_CAM_PROPS == 1:
            self.THREAD_CAMERA_1.cap.set(cv2.CAP_PROP_SETTINGS, 1)
        self.THREAD_CAMERA_1.update_error_signal.connect(
            self.update_status_camera_error
        )
        # thread camera 2
        self.THREAD_CAMERA_2 = CameraThread(self.ID_C2)
        self.THREAD_CAMERA_2.frame_received.connect(self.display_frame2)
        self.THREAD_CAMERA_2.start()
        self.THREAD_CAMERA_2.cap.set(cv2.CAP_PROP_EXPOSURE, self.PROP_EXPOSURE_2)

        if self.IS_OPEN_CAM_PROPS == 1:
            self.THREAD_CAMERA_2.cap.set(cv2.CAP_PROP_SETTINGS, 1)
        self.THREAD_CAMERA_2.update_error_signal.connect(
            self.update_status_camera_error
        )

        set_default_state(self)
        self.set_default_variables()

    def reconnect_camera_thread(self):
        try:
            if (
                len(self.graph.get_input_devices()) == self.NUM_CAMERA
                and not self.THREAD_CAMERA_1.is_running
                and not self.THREAD_CAMERA_2.is_running
            ):
                print("re open")
                self.open_camera_thread()
        except Exception as E:
            cmd_printer("ERROR", str(E))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    sys.exit(app.exec_())
