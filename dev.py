from skimage.metrics import structural_similarity as ssim
import cv2


def compare_images_ssim(image1_path, image2_path):
    img1 = cv2.imread(image1_path, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(image2_path, cv2.IMREAD_GRAYSCALE)

    similarity_index, _ = ssim(img1, img2, full=True)

    similarity_percentage = similarity_index * 100
    print(f"Percent matching (SSIM): {similarity_percentage:.2f}%")


image1_path = "./test 2.png"
image2_path = "./test 3.png"

compare_images_ssim(image1_path, image2_path)


def detect_position_