import cv2
import numpy as np


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
    """
    :param float a max-value for threshhold
    :param float c ...
    """
    height, width = img.shape[:2]
    border_size = 20
    corners = np.array([
        [0, 0],              # Верхний-левый
        [width - 1, 0],       # Верхний-правый
        [width - 1, height - 1],  # Нижний-правый
        [0, height - 1]       # Нижний-левый
    ], dtype="int")

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
    return order_points(screenCnt.reshape(4, 2), type="int32")
    # return screenCnt.reshape(4, 2)


def four_point_transform(image, pts):
    """Точное перспективное преобразование по 4 точкам"""
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Вычисляем ширину новой изображения
    width_a = np.linalg.norm(br - bl)
    width_b = np.linalg.norm(tr - tl)
    max_width = max(int(width_a), int(width_b))

    # Вычисляем высоту новой изображения
    height_a = np.linalg.norm(tr - br)
    height_b = np.linalg.norm(tl - bl)
    max_height = max(int(height_a), int(height_b))

    # Точки назначения
    dst = np.array([
        [0, 0],
        [max_width - 1, 0],
        [max_width - 1, max_height - 1],
        [0, max_height - 1]], dtype="float32")

    # Перспективное преобразование
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(
        image, M, (max_width, max_height),
        flags=cv2.INTER_LINEAR,
        borderMode=cv2.BORDER_CONSTANT,
        borderValue=(255, 255, 255)
    )
    return warped


def order_points(pts, type="float32"):
    # Сортируем точки по x-координате
    x_sorted = pts[np.argsort(pts[:, 0]), :]

    # Разделяем на левые и правые точки
    left_most = x_sorted[:2, :]
    right_most = x_sorted[2:, :]

    # Сортируем левые точки по y (верх-лев, низ-лев)
    left_most = left_most[np.argsort(left_most[:, 1]), :]
    tl, bl = left_most

    # Сортируем правые точки по y (верх-прав, низ-прав)
    right_most = right_most[np.argsort(right_most[:, 1]), :]
    tr, br = right_most

    return np.array([tl, tr, br, bl], dtype=type)


def align_img(image, contour):
    """Полный процесс выравнивания документа"""
    # 1. Пытаемся найти контур страницы
    ordered_contour = order_points(contour)
    aligned = four_point_transform(image, ordered_contour.reshape(4, 2))
    return aligned


def preprocess_img(image):
    return align_img(image, find_page_contour(image, a=180, c=5))


def enhance_text_readability(image, scale_factor=1, sharpening_strength=1.3, denoise_level=1):
    """
    Улучшает читаемость текста на изображении

    Параметры:
    - image: входное изображение (numpy array)
    - scale_factor: коэффициент увеличения (рекомендуется 1.0-1.5)
    - sharpening_strength: сила повышения резкости (1.0-2.0)
    - denoise_level: уровень подавления шумов (1-10)

    Возвращает:
    - Улучшенное изображение
    """
    if image is None:
        raise ValueError("Не удалось загрузить изображение")

    # 1. Увеличение разрешения с сохранением деталей
    if scale_factor != 1.0:
        high_res = cv2.resize(image, None, fx=scale_factor, fy=scale_factor,
                              interpolation=cv2.INTER_CUBIC)
    else:
        high_res = image.copy()

    # 2. Преобразование в LAB цветовое пространство для работы с яркостью
    lab = cv2.cvtColor(high_res, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # 3. Адаптивное улучшение контраста только для канала яркости
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_l = clahe.apply(l_channel)

    # 4. Подавление шумов
    denoised = cv2.fastNlMeansDenoising(enhanced_l, None, h=denoise_level,
                                        templateWindowSize=7,
                                        searchWindowSize=21)

    # 5. Повышение резкости с регулируемой силой
    kernel_size = int(3 * sharpening_strength)
    if kernel_size % 2 == 0:
        kernel_size += 1

    sharpened = cv2.GaussianBlur(denoised, (0, 0), kernel_size)
    sharpened = cv2.addWeighted(denoised, 1.0 + sharpening_strength,
                                sharpened, -sharpening_strength, 0)

    # 6. Сборка финального изображения
    merged_lab = cv2.merge((sharpened, a, b))
    final = cv2.cvtColor(merged_lab, cv2.COLOR_LAB2BGR)

    return final
