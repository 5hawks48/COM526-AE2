import operator
import os

import cv2
import numpy as np
import random as rng


def read_img():
    # I wanted the user to have the liberty to choose the image
    image_url = r"ImageRecognition\sudoku.jpg"
    # image url also conatins the image extension eg. .jpg or .png
    # reading in greayscale
    img = cv2.imread(image_url, cv2.IMREAD_GRAYSCALE)
    cv2.imshow('image', img)
    cv2.waitKey(0)
    return img


def gaussian_blur(img):
    processed_img = cv2.GaussianBlur(img.copy(), (9, 9), 0)

    # cv2.adaptiveThreshold(src, maxValue, adaptiveMethod, thresholdType, blockSize, constant(c))
    # blockSize – Size of a pixel neighborhood that is used to calculate a threshold value for the pixel: 3, 5, 7, and so on.
    # C – Constant subtracted from the mean or weighted mean (see the details below). Normally, it is positive but may be zero or negative as well.
    processed_img = cv2.adaptiveThreshold(processed_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    processed_img = cv2.bitwise_not(processed_img, processed_img)

    # np.uint8 will wrap.
    # For example, 235+30 = 9.
    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
    processed_img = cv2.dilate(processed_img, kernel)

    cv2.imshow('inverted', processed_img)
    cv2.waitKey(0)

    return processed_img


def find_contours(process):
    ext_contours, hierarchy = cv2.findContours(process, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # for c in ext_contours:
    #     peri = cv2.arcLength(c, True)
    #     approx = cv2.approxPolyDP(c, 0.015 * peri, True)
    #     if len(approx) == 4:
    #         # Here we are looking for the largest 4 sided contour
    #         break

    # Draw contours
    drawing = np.zeros((process.shape[0], process.shape[1], 3), dtype=np.uint8)
    for i in range(len(ext_contours)):
        color = (rng.randint(0, 256), rng.randint(0, 256), rng.randint(0, 256))
        cv2.drawContours(drawing, ext_contours, i, color, 2, cv2.LINE_8, hierarchy, 0)
    # Show in a window
    cv2.imshow('Contours', drawing)
    cv2.waitKey(0)
    return ext_contours


def find_corners_approxPolyDP(ext_contours):
    # ext_contours = ext_contours[0] if len(ext_contours) == 2 else ext_contours[1]
    cnts = sorted(ext_contours, key=cv2.contourArea, reverse=True)[:5]
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.015 * peri, True)
        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            return approx


def extract_points(corners):
    # Extracting the points
    corners = [(corner[0][0], corner[0][1]) for corner in corners]
    top_r, top_l, bottom_l, bottom_r = corners[0], corners[1], corners[2], corners[3]
    return top_l, top_r, bottom_r, bottom_l  # Index 0 - top-right
    #       1 - top-left
    #       2 - bottom-left
    #       3 - bottom-right


def find_corners_Ramer_Doughlas_Peucker(ext_contours):
    bottom_right, _ = max(enumerate([pt[0][0] + pt[0][1] for pt in ext_contours[0]]), key=operator.itemgetter(1))
    top_left, _ = min(enumerate([pt[0][0] + pt[0][1] for pt in ext_contours[0]]), key=operator.itemgetter(1))
    bottom_left, _ = min(enumerate([pt[0][0] - pt[0][1] for pt in ext_contours[0]]), key=operator.itemgetter(1))
    top_right, _ = max(enumerate([pt[0][0] - pt[0][1] for pt in ext_contours[0]]), key=operator.itemgetter(1))
    return top_left, top_right, bottom_right, bottom_left


def crop_and_warp(image, ordered_corners, bottom_r, bottom_l, top_r, top_l):
    width_A = np.sqrt(((bottom_r[0] - bottom_l[0]) ** 2) + ((bottom_r[1] - bottom_l[1]) ** 2))
    width_B = np.sqrt(((top_r[0] - top_l[0]) ** 2) + ((top_r[1] - top_l[1]) ** 2))
    width = max(int(width_A), int(width_B))
    height_A = np.sqrt(((top_r[0] - bottom_r[0]) ** 2) + ((top_r[1] - bottom_r[1]) ** 2))
    height_B = np.sqrt(((top_l[0] - bottom_l[0]) ** 2) + ((top_l[1] - bottom_l[1]) ** 2))
    height = max(int(height_A), int(height_B))

    dimensions = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1],
                           [0, height - 1]], dtype="float32")
    # Convert to Numpy format
    ordered_corners = np.array(ordered_corners, dtype="float32")  # calculate the perspective transform matrix and warp
    # the perspective to grab the screen
    grid = cv2.getPerspectiveTransform(ordered_corners, dimensions)
    return cv2.warpPerspective(image, grid, (width, height))


def create_image_grid(grid):
    # here grid is the cropped image

    # grid = cv2.cvtColor(grid, cv2.COLOR_BGR2GRAY)  # VERY IMPORTANT

    # Adaptive thresholding the cropped grid and inverting it
    grid = cv2.bitwise_not(cv2.adaptiveThreshold(grid, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 101, 1))
    cv2.imshow('cells', grid)
    cv2.waitKey(0)
    grid = extract_squares(grid)
    return grid


def extract_squares(grid):
    edge_h = np.shape(grid)[0]
    edge_w = np.shape(grid)[1]
    celledge_h = edge_h // 9
    celledge_w = np.shape(grid)[1] // 9
    tempgrid = []
    for i in range(celledge_h, edge_h + 1, celledge_h):
        for j in range(celledge_w, edge_w + 1, celledge_w):
            rows = grid[i - celledge_h:i]
            tempgrid.append([rows[k][j - celledge_w:j] for k in range(len(rows))])
    # Creating the 9X9 grid of images
    finalgrid = []
    for i in range(0, len(tempgrid) - 8, 9):
        finalgrid.append(tempgrid[i:i + 9])  # Converting all the cell images to np.array
    for i in range(9):
        for j in range(9):
            finalgrid[i][j] = np.array(finalgrid[i][j])
    try:
        for i in range(9):
            for j in range(9):
                os.remove("BoardCells/cell" + str(i) + str(j) + ".jpg")
    except:
        pass
    for i in range(9):
        for j in range(9):
            cv2.imwrite(str("BoardCells/cell" + str(i) + str(j) + ".jpg"), finalgrid[i][j])
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


def extract():
    print("Read img")
    img = read_img()
    print("Gaussian blue img")
    process = gaussian_blur(img)

    # edges = cv2.Canny(process, 100, 200)
    print("Find contours")
    contours = find_contours(process)
    print("Find corners")
    corners = find_corners_approxPolyDP(contours)
    cornerImg = cv2.drawContours(img, corners, -1, (0, 255, 0), 3)
    cv2.imshow("Corners", cornerImg)
    cv2.waitKey(0)

    print("Extract points")
    top_l, top_r, bottom_r, bottom_l = extract_points(corners)
    top_l2, top_r2, bottom_r2, bottom_l2 = find_corners_Ramer_Doughlas_Peucker(contours)

    print("Crop and Warp")
    # Clockwise Corners
    ordered_corners = [top_l, top_r, bottom_r, bottom_l]
    transformed = crop_and_warp(img, ordered_corners, bottom_r, bottom_l, top_r, top_l)
    cropped = r'ImageRecognition/cropped_img.png'
    cv2.imwrite(cropped, transformed)
    transformed = cv2.resize(transformed, (450, 450))
    cv2.imshow(r'ImageRecognition/cropped_img', transformed)
    cv2.waitKey(0)

    print("Extract cells")
    final_grid = create_image_grid(transformed)
    cv2.imshow('cell[2][0]', final_grid[2][0])
    cv2.waitKey(0)

    # corners = find_corners(contours)

    # ## Working edges algo
    # contour = max(contours, key=len)
    # print("Contour: " + str(contour))
    # contourImg = cv2.drawContours(img, contour, -1, (0, 255, 0), 3)
    # cv2.imshow("Contours", contourImg)
    # cv2.waitKey(0)

    cv2.destroyAllWindows()
    return final_grid


if __name__ == "__main__":
    extract()