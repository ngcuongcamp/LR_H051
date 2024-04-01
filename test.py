import cv2

# Đọc hình ảnh
image = cv2.imread(r"./mold_code_1.png", 0)  # Ảnh đen trắng, 0: grayscale

# Áp dụng adaptive threshold
adaptive_threshold = cv2.adaptiveThreshold(
    image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 61, 2
)


# Hiển thị hình ảnh gốc và hình ảnh sau khi áp dụng adaptive threshold
cv2.imshow("Original Image", image)
cv2.imshow("Adaptive Threshold", adaptive_threshold)
cv2.waitKey(0)
cv2.destroyAllWindows()
