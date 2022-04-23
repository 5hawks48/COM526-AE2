"""
Image recognition for Sudoku puzzles based off of
Article: https://becominghuman.ai/image-processing-sudokuai-opencv-45380715a629
Article author: Aditi Jain
"""

import cv2
import numpy as np


def display_image(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    cv2.destroyWindow(name)


def invert_and_dilate(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Note that kernel sizes must be positive and odd and the kernel must be square.
    process = cv2.GaussianBlur(img.copy(), (9, 9), 0)
    process = cv2.adaptiveThreshold(process, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    process = cv2.bitwise_not(process, process)
    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
    process = cv2.dilate(process, kernel)
    return process


def find_corners(img):
    ext_contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    ext_contours = ext_contours[0] if len(ext_contours) == 2 else ext_contours[1]
    ext_contours = sorted(ext_contours, key=cv2.contourArea, reverse=True)

    # loop runs only once
    for c in ext_contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        if len(approx) == 4:
            # Here we are looking for the largest 4 sided contour
            return approx


# def Ramer_Doughlas_Peucker_algorithm(img):
#     ext_contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     ext_contours = ext_contours[0] if len(ext_contours) == 2 else ext_contours[1]
#     ext_contours = sorted(ext_contours, key=cv2.contourArea, reverse=True)
#     import operator
#     bottom_r, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in ext_contours[0]]), key=operator.itemgetter(1))
#     top_l, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in ext_contours[0]]), key=operator.itemgetter(1))
#     bottom_l, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in ext_contours[0]]), key=operator.itemgetter(1))
#     top_r, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in ext_contours[0]]), key=operator.itemgetter(1))
#     return top_l, top_r, bottom_r, bottom_l


def clockwise_corners(corners):
    """
    https://stackoverflow.com/a/51075698
    -135* --> -180*
    :param corners:
    :return:
    """
    from functools import reduce
    import operator
    import math
    coords = [(corner[0][0], corner[0][1]) for corner in corners]
    center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), coords), [len(coords)] * 2))
    ordered = sorted(coords, key=lambda coord: (-180 - math.degrees(math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)
    # print(ordered)
    top_l, top_r, bottom_r, bottom_l = ordered[0], ordered[1], ordered[2], ordered[3]
    return top_l, top_r, bottom_r, bottom_l


def anticlockwise_corners(corners):
    return clockwise_corners(corners)[::-1]


def order_corners(corners):
    # Corners[0],... stores in format [[x y]]
    # Separate corners into individual points
    # Index 0 - top-right
    #       1 - top-left
    #       2 - bottom-left
    #       3 - bottom-right
    print("Corners before:" + str(corners))
    corners = [(corner[0][0], corner[0][1]) for corner in corners]
    top_r, top_l, bottom_l, bottom_r = corners[0], corners[1], corners[2], corners[3]
    print("Corners after:" + str([top_l, top_r, bottom_r, bottom_l]))
    return top_l, top_r, bottom_r, bottom_l


def crop_and_warp(image, corners):
    """

    :param image:
    :param corners:
    :return:
    """
    # Order points in clockwise order
    # ordered_corners = order_corners(corners)
    # ordered_corners = clockwise_corners(corners)
    ordered_corners = anticlockwise_corners(corners)
    # print(ordered_corners)
    top_l, top_r, bottom_r, bottom_l = ordered_corners

    width_A = np.sqrt(((bottom_r[0] - bottom_l[0]) ** 2) + ((bottom_r[1] - bottom_l[1]) ** 2))
    width_B = np.sqrt(((top_r[0] - top_l[0]) ** 2) + ((top_r[1] - top_l[1]) ** 2))
    width = max(int(width_A), int(width_B))
    height_A = np.sqrt(((top_r[0] - bottom_r[0]) ** 2) + ((top_r[1] - bottom_r[1]) ** 2))
    height_B = np.sqrt(((top_l[0] - bottom_l[0]) ** 2) + ((top_l[1] - bottom_l[1]) ** 2))
    height = max(int(height_A), int(height_B))
    dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1],
                           [0, height - 1]], dtype="float32")
    # Convert to Numpy format
    ordered_corners = np.array(ordered_corners, dtype="float32")
    # calculate the perspective transform matrix and warp
    # the perspective to grab the screen
    grid = cv2.getPerspectiveTransform(ordered_corners, dimensions)
    return cv2.warpPerspective(image, grid, (width, height))


def create_cells(img):
    grid = np.copy(img)
    edge_h = np.shape(grid)[0]
    edge_w = np.shape(grid)[1]
    celledge_h = edge_h // 9
    celledge_w = np.shape(grid)[1] // 9

    grid = cv2.cvtColor(grid, cv2.COLOR_BGR2GRAY)

    # Adaptive thresholding the cropped grid and inverting it
    # grid = cv2.bitwise_not(grid, grid)

    # Adaptive thresholding the cropped grid and inverting it
    grid = cv2.bitwise_not(cv2.adaptiveThreshold(grid, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 1))

    display_image("create_image_grid", grid)

    tempgrid = []
    for i in range(celledge_h, edge_h + 1, celledge_h):
        for j in range(celledge_w, edge_w + 1, celledge_w):
            rows = grid[i - celledge_h:i]
            tempgrid.append([rows[k][j - celledge_w:j] for k in range(len(rows))])

    # Creating the 9X9 grid of images
    finalgrid = []
    for i in range(0, len(tempgrid) - 8, 9):
        finalgrid.append(tempgrid[i:i + 9])

    # Converting all the cell images to np.array
    for i in range(9):
        for j in range(9):
            finalgrid[i][j] = np.array(finalgrid[i][j])

    try:
        for i in range(9):
            for j in range(9):
                np.os.remove(r"ImageRecognition/BoardCells/cell" + str(i) + str(j) + ".jpg")
    except:
        pass
    for i in range(9):
        for j in range(9):
            cv2.imwrite(str(r"ImageRecognition/BoardCells/cell" + str(i) + str(j) + ".jpg"), finalgrid[i][j])

    return finalgrid


def scale_and_centre(img, size, margin=20, background=0):
    """Scales and centres an image onto a new background square."""
    h, w = img.shape[:2]

    def centre_pad(length):
        """Handles centering for a given length that may be odd or even."""
        if length % 2 == 0:
            side1 = int((size - length) / 2)
            side2 = side1
        else:
            side1 = int((size - length) / 2)
            side2 = side1 + 1
        return side1, side2

    def scale(r, x):
        return int(r * x)

    if h > w:
        t_pad = int(margin / 2)
        b_pad = t_pad
        ratio = (size - margin) / h
        w, h = scale(ratio, w), scale(ratio, h)
        l_pad, r_pad = centre_pad(w)
    else:
        l_pad = int(margin / 2)
        r_pad = l_pad
        ratio = (size - margin) / w
        w, h = scale(ratio, w), scale(ratio, h)
        t_pad, b_pad = centre_pad(h)

    img = cv2.resize(img, (w, h))
    img = cv2.copyMakeBorder(img, t_pad, b_pad, l_pad, r_pad, cv2.BORDER_CONSTANT, None, background)
    return cv2.resize(img, (size, size))


def extract(img):
    processed_sudoku = invert_and_dilate(img)
    corners = find_corners(processed_sudoku)
    display_image("corners", cv2.drawContours(img, corners, -1, (0, 255, 0), 10))
    transformed = crop_and_warp(img, corners)
    display_image("transformed", transformed)
    cropped = r'ImageRecognition/cropped_img.png'
    cv2.imwrite(cropped, transformed)
    transformed = cv2.resize(transformed, (450, 450))
    sudoku = create_cells(transformed)
    return sudoku


def run(img_path, guess_type):
    from ImageRecognition.digit_recognition import run as create_and_save_Model
    from ImageRecognition.predict import extract_number_image as sudoku_extracted
    import solver

    print("Running image recognition...")
    # Sudoku extract
    # Calling the image_prcoesses.py extract function to get a processed np.array of cells
    base_img = cv2.imread(img_path)
    if base_img is None:
        raise FileNotFoundError('The image with path "' + str(img_path) + '" could not be found')
    image_grid = extract(base_img)
    # image_grid = image_processing.extract()
    print("Image Grid extracted...")

    # note we have alreday created and stored the model but if you want to do that again use the following command
    # create_and_save_Model()

    # Sudoku extract
    sudoku = sudoku_extracted(image_grid)
    print("Extracted and predict digits in the Sudoku")
    print("\n\nSudoku:")
    solver.print_grid(sudoku)
    solved, backtracks = solver.solve(sudoku, 0, guess_type, False)
    solver.print_grid(sudoku)
    print("Solved = %s, Backtracks =  %d" % (solved, backtracks))
    print("Image recognition finished.")
