from libs.libs import *
from src.utilities import *
from src.Thread_PLC import PLCThread
from src.Thread_Camera import CameraThread
from src.connect_mes import *
from src.reader import *
from src.UI_handler import *
from src.capture_and_compare import *
from src.Worker_locate import *


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
        self.is_pushing = False

        initial_UI_MainWindow(self)  # initialize UI
        read_config(self)  # read config

        #! TEST REPAINT
        if self.IS_USE_REPAINT == 1:
            self.timer_to_repaint = QTimer(self)
            self.timer_to_repaint.timeout.connect(self.repaint_ui)
            self.timer_to_repaint.start(10000)

        #! TEST MINIMIZE WINDOW
        if self.IS_USE_MINIMIZE == 1:
            self.minimize_timer_running = True
            self.timer_to_minimize = QTimer(self)
            self.timer_to_minimize.timeout.connect(self.minimize_ui)
            # 3 mins to refresh
            self.timer_to_minimize.start(3 * 60 * 1000)
            # self.timer_to_minimize.start(5000)

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

    # def handle_click_update(self, event):
    #     req = QMessageBox.question(
    #         self,
    #         "Confirm Update",
    #         "Do you want to update latest version?",
    #         QMessageBox.Yes | QMessageBox.No,
    #         QMessageBox.No,
    #     )
    #     if req == QMessageBox.Yes:
    #         cmd_printer("WARNING", "Handler update function here...")

    #         req3 = QMessageBox.warning(
    #             self, "Information", "Not found latest version!", QMessageBox.Cancel
    #         )
    #     else:
    #         print("Ignore update")

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
        start_time_read = time.time()
        self.set_default_variables()

        if self.IS_USE_DYNAMIC_FRAME != 1:
            self.state_ui = None
            set_default_state(self)
            self.Show_frame1(None)
            self.Show_frame2(None)
        i = 0
        while i < self.SCAN_LIMIT:  # 3
            print("stt loop: ", i + 1)
            i = i + 1
            if self.data_scan1 is None:
                frames = process_frame1(self, self.frame1)
                self.data_scan1, point1 = read_code_zxingcpp(frames)
                if self.data_scan1 is None:
                    self.data_scan1, point1 = loop_thresh_frame(
                        self,
                        frames,
                        self.MIN_THRESH_1,
                        self.MAX_THRESH_1,
                        self.SPACE_THRESH_1,
                    )
                if self.data_scan1 and self.IS_USE_DYNAMIC_FRAME != 1:
                    self.Show_frame1(point1)

            if self.data_scan2 is None:
                frames2 = process_frame2(self, self.frame2)
                self.data_scan2, point2 = read_code_zxingcpp(frames2)
                if self.data_scan2 is None:
                    self.data_scan2, point2 = loop_thresh_frame(
                        self,
                        frames2,
                        self.MIN_THRESH_2,
                        self.MAX_THRESH_2,
                        self.SPACE_THRESH_2,
                    )
                if self.data_scan2 and self.IS_USE_DYNAMIC_FRAME != 1:
                    self.Show_frame2(point2)

            if self.data_scan1 is not None and self.data_scan2 is not None:
                break

        print("--> RESULT SCAN")
        logger.info("--> RESULT SCAN")

        # IF FAIL SCAN
        if self.data_scan1 is None or self.data_scan2 is None:
            self.state_ui = None

            if self.data_scan1 is None:
                if self.state_ui in [True, None]:
                    set_fail_state(self, "FAIL SN")
                    try:
                        self.update()
                    except Exception as E:
                        print(E)
                    self.state_ui = False

            if self.data_scan2 is None:
                if self.state_ui in [True, None]:
                    set_fail_state(self, "FAIL FIXTURE")
                    try:
                        self.update()
                    except Exception as E:
                        print(E)
                    self.state_ui = False

            # cmd_printer("ERROR", "FAILED SCAN")
            logger.error("FAILED")
            self.THREAD_PLC.send_signal_to_plc(b"2")
            self.is_processing = False
            if self.IS_SAVE_NG_IMAGE == 1:
                if self.data_scan1 is None:
                    cmd_printer("ERROR", "FAILED SCAN SN")
                    image_filename = "image_NG/{}/CAMERA1/{}.png".format(
                        get_current_date(), format_current_time()
                    )
                    cv2.imwrite(image_filename, self.frame1)
                if self.data_scan2 is None:

                    cmd_printer("ERROR", "FAILED SCAN FIXTURE")
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

        # IF PASS SCAN
        if self.data_scan1 is not None and self.data_scan2 is not None:
            self.state_ui = None
            is_matching_1 = None
            is_matching_2 = None
            cmd_printer("SUCCESS", "PASS SCAN")
            logger.info("PASS SCAN")
            print(f"Data SN: {self.data_scan1}")
            print(f"Data FIXTURE: {self.data_scan2}")

            print("----------- SEND TO MES -----------")
            logger.info("----------- SEND TO MES -----------")

            self.is_pushing = True

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
                    set_fail_state(self, "FAIL MES")
                    try:
                        self.update()
                    except Exception as E:
                        print(E)
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
                    cmd_printer("ERROR", "SIGNAL FAIL CHECK FIXTURE CODE FROM mes")
                    if self.state_ui in [True, None]:
                        set_fail_state(self, "FAIL MES")
                        try:
                            self.update()
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
                        except Exception as E:
                            print(E)
                        self.state_ui = True
                    self.set_default_variables()

            self.is_pushing = False
        print(f"use {time.time() - start_time_read} to process")

    def set_default_variables(self):
        self.data_scan1 = None
        self.data_scan2 = None
        self.result_mes_operation = [False, False]

    def display_frame1(self, frame):
        self.frame1 = frame
        if self.IS_USE_DYNAMIC_FRAME == 1:
            frame_rgb = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)
            img = QImage(
                frame_rgb.data,
                frame_rgb.shape[1],
                frame_rgb.shape[0],
                QImage.Format_RGB888,
            )
            scaled_pixmap = img.scaled(self.Uic.CameraFrame1.size())
            pixmap = QPixmap.fromImage(scaled_pixmap)
            self.Uic.CameraFrame1.setPixmap(pixmap)

    def Show_frame1(self, point):
        frame_rgb = cv2.cvtColor(self.frame1, cv2.COLOR_BGR2RGB)
        if self.data_scan1 is not None:
            for i in range(len(point) - 1):
                cv2.line(frame_rgb, point[i], point[i + 1], (0, 255, 0), 5)
            cv2.line(frame_rgb, point[-1], point[0], (0, 255, 0), 5)
        img = QImage(
            frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888
        )
        scaled_pixmap = img.scaled(self.Uic.CameraFrame1.size())
        pixmap = QPixmap.fromImage(scaled_pixmap)
        self.Uic.CameraFrame1.setPixmap(pixmap)

    def display_frame2(self, frame):
        self.frame2 = frame
        if self.IS_USE_DYNAMIC_FRAME == 1:
            frame_rgb = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
            img = QImage(
                frame_rgb.data,
                frame_rgb.shape[1],
                frame_rgb.shape[0],
                QImage.Format_RGB888,
            )
            scaled_pixmap = img.scaled(self.Uic.CameraFrame2.size())
            pixmap = QPixmap.fromImage(scaled_pixmap)
            self.Uic.CameraFrame2.setPixmap(pixmap)

    def Show_frame2(self, point):
        frame_rgb = cv2.cvtColor(self.frame2, cv2.COLOR_BGR2RGB)
        if self.data_scan2 is not None:
            for i in range(len(point) - 1):
                cv2.line(frame_rgb, point[i], point[i + 1], (0, 255, 0), 5)
            cv2.line(frame_rgb, point[-1], point[0], (0, 255, 0), 5)
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
        self.THREAD_CAMERA_1.cap.set(cv2.CAP_PROP_EXPOSURE, self.PROP_EXPOSURE_2)

        if self.IS_OPEN_CAM_PROPS == 1:
            self.THREAD_CAMERA_2.cap.set(cv2.CAP_PROP_SETTINGS, 1)
        self.THREAD_CAMERA_2.update_error_signal.connect(
            self.update_status_camera_error
        )

        set_default_state(self)
        self.set_default_variables()

    def reconnect_camera_thread(self):
        # test always update with update medthod
        # self.update()
        try:
            self.update()
        except Exception as E:
            print(E)
        if (
            self.THREAD_CAMERA_1.is_running == False
            or self.THREAD_CAMERA_2.is_running == False
        ):
            self.THREAD_CAMERA_1.stop()
            self.THREAD_CAMERA_2.stop()

        try:
            if (
                len(self.graph.get_input_devices()) == self.NUM_CAMERA
                and self.THREAD_CAMERA_1.is_running == False
                and self.THREAD_CAMERA_2.is_running == False
            ):
                self.open_camera_thread()
        except Exception as E:
            cmd_printer("ERROR", str(E))

    # def paintEvent(self, event):

    def repaint_ui(self):
        try:
            print("repaint ui")
            self.Uic.CameraFrame1.repaint()
            self.Uic.CameraFrame2.repaint()
            self.Uic.ResultSpan.repaint()
        except Exception as E:
            print("Error repaint: ", E)

    def minimize_ui(self):
        if self.minimize_timer_running:
            self.timer_to_minimize.stop()
            self.minimize_timer_running = False

            stime = time.time()
            try:
                if self.is_pushing == False:
                    print("minimize_ui called!")
                    self.hide()
                    self.show()
                elif self.is_pushing == True:
                    while self.is_pushing == True and time.time() - stime <= 2:
                        time.sleep(0.2)
                        if self.is_pushing == False:
                            print("minimize_ui called!")
                            self.hide()
                            self.show()
                            break

                self.timer_to_minimize.start(3 * 60 * 1000)
                # self.timer_to_minimize.start(5000)
                self.minimize_timer_running = True

            except Exception as E:
                print(E)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApplication()
    sys.exit(app.exec_())
