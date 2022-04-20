"""
Image recognition for Sudoku puzzles based off of
Article: https://becominghuman.ai/image-processing-sudokuai-opencv-45380715a629
Article author: Aditi Jain
"""
import cv2
import numpy as np
from tensorflow.python.keras.models import load_model
import matplotlib.pyplot as plt

from ImageRecognition.image_processing import scale_and_centre, order_corners, extract


def display_image(img):
    cv2.imshow('image', img)  # Display the image
    cv2.waitKey(0)  # Wait for any key to be pressed (with the image window active)
    cv2.destroyAllWindows()  # Close all windows


def extract_number_image(img_grid):
    tmp_sudoku = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        for j in range(9):

            image = img_grid[i][j]
            image = cv2.resize(image, (28, 28))
            original = image.copy()

            thresh = 128  # define a threshold, 128 is the middle of black and white in grey scale
            # threshold the image
            gray = cv2.threshold(image, thresh, 255, cv2.THRESH_BINARY)[1]

            # Find contours
            cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]

            for c in cnts:
                x, y, w, h = cv2.boundingRect(c)

                if (x < 3 or y < 3 or h < 3 or w < 3):
                    continue
                ROI = gray[y:y + h, x:x + w]
                ROI = scale_and_centre(ROI, 120)
                # display_image(ROI)

                # Writing the cleaned cells
                cv2.imwrite(r"ImageRecognition/CleanedBoardCells/cell{}{}.png".format(i, j), ROI)
                tmp_sudoku[i][j] = predict(ROI)

    return tmp_sudoku


def predict(img_grid):
    image = img_grid.copy()
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY)[1]
    image = cv2.resize(image, (28, 28))
    image = image.astype('float32')
    image = image.reshape(1, 28, 28, 1)
    image /= 255
    # plt.imshow(image.reshape(28, 28), cmap='Greys')
    # plt.show()
    model = load_model(r'ImageRecognition/cnn.hdf5')
    pred = model.predict(image.reshape(1, 28, 28, 1), batch_size=1)

    # print("Predicted number: " + str(pred.argmax()))

    return pred.argmax()

# extract_number_image(extract())
