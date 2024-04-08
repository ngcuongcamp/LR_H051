from libs.libs import cv2, ZBarSymbol, decode, zxingcpp

path_dir = r"./libs/opencv_3rdparty-wechat_qrcode"
detect_model = path_dir + "/detect.caffemodel"
detect_protox = path_dir + "/detect.prototxt"
sr_model = path_dir + "/sr.caffemodel"
sr_protox = path_dir + "/sr.prototxt"
detector = cv2.wechat_qrcode_WeChatQRCode(
    detect_protox, detect_model, sr_protox, sr_model
)


def read_code_wechat(frames):
    for frame in frames:
        data, points = detector.detectAndDecode(frame)
        if len(data) > 0:
            bbox = [points[0].astype(int)]
            points = [bbox[0][0], bbox[0][1], bbox[0][2], bbox[0][3]]
            return data[0], points
    return None, None


def read_code_pyzbar(frames):
    for frame in frames:
        decoded_data = decode(frame, symbols=[ZBarSymbol.QRCODE])
        if len(decoded_data) > 0:
            points = [
                (decoded_data[0].polygon[0].x, decoded_data[0].polygon[0].y),
                (decoded_data[0].polygon[1].x, decoded_data[0].polygon[1].y),
                (decoded_data[0].polygon[2].x, decoded_data[0].polygon[2].y),
                (decoded_data[0].polygon[3].x, decoded_data[0].polygon[3].y),
            ]
            return decoded_data[0].data.decode("utf-8"), points
    return read_code_wechat(frames)


def read_code_zxingcpp(frames):
    for frame in frames:
        data_decodeded = zxingcpp.read_barcodes(frame)
        if len(data_decodeded) > 0:
            coord_pairs = str(data_decodeded[0].position)
            cleaned_pairs = coord_pairs.replace("\x00", "")
            points = [
                tuple(map(int, pair.split("x"))) for pair in cleaned_pairs.split()
            ]
            return data_decodeded[0].text, points
    return read_code_pyzbar(frames)


def process_frame1(self, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    opened = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, (3, 3))
    erosion = cv2.erode(opened, (3, 3), iterations=1)
    dilation = cv2.dilate(opened, (3, 3), iterations=1)
    return [gray, opened, erosion, dilation]


def process_frame2(self, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    opened = cv2.morphologyEx(blurred, cv2.MORPH_OPEN, (3, 3))
    erosion = cv2.erode(opened, (3, 3), iterations=1)
    dilation = cv2.dilate(opened, (3, 3), iterations=1)
    return [gray, opened, erosion, dilation]


def loop_thresh_frame(self, frames, min_thresh, max_thresh, space_thresh):
    data = None
    for frame in frames:
        print("for running")
        for thresh_value in range(min_thresh, max_thresh, space_thresh):

            _, thresh_frame = cv2.threshold(
                frame, thresh_value, max_thresh, cv2.THRESH_BINARY
            )
            data, point = read_code_zxingcpp([thresh_frame])

            if data is not None:
                print("thresh value: ", thresh_value)
                return data, point

        if data is not None:
            break
    return None, None
