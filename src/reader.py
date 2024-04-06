from libs.libs import cv2, ZBarSymbol, decode, zxingcpp

path_dir = r"./libs/opencv_3rdparty-wechat_qrcode"
detect_model = path_dir + "/detect.caffemodel"
detect_protox = path_dir + "/detect.prototxt"
sr_model = path_dir + "/sr.caffemodel"
sr_protox = path_dir + "/sr.prototxt"
detector = cv2.wechat_qrcode_WeChatQRCode(
    detect_protox, detect_model, sr_protox, sr_model
)


# def read_code_wechat(frames):
#     for frame in frames:
#         data, points = detector.detectAndDecode(frame)
#         if len(data) > 0:
#             return data[0]
#     return read_code_pyzbar(frames)


# def read_code_pyzbar(frames):
#     for frame in frames:
#         decoded_data = decode(frame, symbols=[ZBarSymbol.QRCODE])
#         if len(decoded_data) > 0:
#             return decoded_data[0].data.decode("utf-8")
#     return read_code_zxingcpp(frames)


# def read_code_zxingcpp(frames):
#     for frame in frames:
#         data_decodeded = zxingcpp.read_barcodes(frame)
#         if len(data_decodeded) > 0:
#             return data_decodeded[0].text
#     return None
def read_code_wechat(frames):
    for frame in frames:
        data, points = detector.detectAndDecode(frame)
        if len(data) > 0:
            bbox = [points[0].astype(int)]
            points = [bbox[0][0], bbox[0][1], bbox[0][2], bbox[0][3]]
            return data[0], points
    # return None, None
    return read_code_pyzbar(frames)


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
    return read_code_zxingcpp(frames)


def read_code_zxingcpp(frames):
    for frame in frames:
        data_decodeded = zxingcpp.read_barcodes(frame)
        if len(data_decodeded) > 0:
            coord_pairs = str(data_decodeded[0].position)
            # print("coord_pairs", coord_pairs)
            cleaned_pairs = coord_pairs.replace("\x00", "")
            points = [
                tuple(map(int, pair.split("x"))) for pair in cleaned_pairs.split()
            ]
            return data_decodeded[0].text, points
    return None, None


def process_frame1(self, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        self.BLOCK_SIZE_1,
        self.C1,
    )

    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (3, 3))
    erosion = cv2.erode(opened, (3, 3), iterations=1)
    dilation = cv2.dilate(opened, (3, 3), iterations=1)
    return [gray, thresh, opened, erosion, dilation]


def process_frame2(self, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
    thresh = cv2.adaptiveThreshold(
        blurred,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        self.BLOCK_SIZE_2,
        self.C2,
    )

    opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, (3, 3))
    erosion = cv2.erode(opened, (3, 3), iterations=1)
    dilation = cv2.dilate(opened, (3, 3), iterations=1)
    return [gray, thresh, opened, erosion, dilation]
