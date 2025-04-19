import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage
import imutils


def add_black_border(image, border_size=20):
    """Adds a black border around the image"""
    return cv2.copyMakeBorder(
        image,
        top=border_size,
        bottom=border_size,
        left=border_size,
        right=border_size,
        borderType=cv2.BORDER_CONSTANT,
        value=[0, 0, 0]  # Black color
    )


def find_page_contour(img, margin=20, a=180, c=5):
    height, width = img.shape[:2]
    border_size = 20
    corners = np.array([
        [0, 0],              # Верхний-левый
        [width - 1, 0],       # Верхний-правый
        [width - 1, height - 1],  # Нижний-правый
        [0, height - 1]       # Нижний-левый
    ], dtype="float32")

    img = add_black_border(img, border_size)
    image = img.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    thresh = cv2.adaptiveThreshold(
        gray, a, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 21, c
    )

    kernel = np.ones((3, 3), np.uint8)
    processed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv2.findContours(processed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Handle OpenCV version difference
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]

    height, width = image.shape[:2]
    image_area = width * height

    screenCnts = []
    screenCnt = None
    for c in cnts:
        area = cv2.contourArea(c)
        if area < image_area * 0.1:  # <10% от площади изображения
            continue

        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:
            # screenCnt = approx
            screenCnts.append(approx)
            break
    good_cnts = screenCnts
    good_cnts = sorted(good_cnts, key=cv2.contourArea, reverse=True)
    if len(good_cnts) >= 2:
        screenCnt = good_cnts[1]
        for i in range(4):
            for j in range(2):
                screenCnt[i][0][j] = max(0, screenCnt[i][0][j] - border_size)
    elif len(good_cnts) == 1:
        screenCnt = good_cnts[0]
        for i in range(4):
            for j in range(2):
                screenCnt[i][0][j] = max(0, screenCnt[i][0][j] - border_size)
    else:
        screenCnt = corners
    return screenCnt
