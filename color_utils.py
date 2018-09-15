import numpy as np
import cv2 as cv

LOWER_RED1 = np.array([0, 100, 120])
UPPER_RED1 = np.array([10, 255, 255])
LOWER_RED2 = np.array([170, 100, 120])
UPPER_RED2 = np.array([180, 255, 255])
LOWER_YELLOW = np.array([20, 100, 100])
UPPER_YELLOW = np.array([40, 255, 255])
LOWER_VIOLET = np.array([101, 100, 100])
UPPER_VIOLET = np.array([121, 255, 255])


def getCorners(mask, img):
    _, contours, _ = cv.findContours(mask, cv.RETR_CCOMP, cv.CHAIN_APPROX_SIMPLE + 2)
    n = len(contours)
    ret = 0
    for i in range(0, len(contours)):
        cnt = contours[i]
        epsilon = 0.03 * cv.arcLength(cnt, True)
        approx = cv.approxPolyDP(cnt, epsilon, True)
        for corner in approx:
            x, y = corner.ravel()
        ret = max(ret, len(approx))
    return ret, img


def get_color(frame):
    global shape
    frame = cv.GaussianBlur(frame, (25, 25), 2)
    frame = cv.dilate(frame, np.ones((15, 15), np.uint8))
    frame = cv.erode(frame, np.ones((15, 15), np.uint8))

    # Converting the colors from RGB to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    # Generating a binary mask for the 3 colors
    mask_red1 = cv.inRange(hsv, LOWER_RED1, UPPER_RED1)
    mask_red2 = cv.inRange(hsv, LOWER_RED2, UPPER_RED2)
    mask_red = cv.bitwise_or(mask_red1, mask_red2)
    mask_yellow = cv.inRange(hsv, LOWER_YELLOW, UPPER_YELLOW)
    mask_violet = cv.inRange(hsv, LOWER_VIOLET, UPPER_VIOLET)

    # Filtering colors
    red_filter = cv.bitwise_and(frame, frame, mask=mask_red)
    yellow_filter = cv.bitwise_and(frame, frame, mask=mask_yellow)
    violet_filter = cv.bitwise_and(frame, frame, mask=mask_violet)

    # Defining contours and count the corners of each contour
    red_corners, red_contours = getCorners(mask_red, red_filter.copy())
    yellow_corners, yellow_contours = getCorners(mask_yellow, yellow_filter.copy())
    violet_corners, violet_contours = getCorners(mask_violet, violet_filter.copy())

    print(red_corners, yellow_corners, violet_corners)

    if red_corners > 7:
        shape = "Z"
    elif yellow_corners > 7:
        shape = "O"
    elif violet_corners > 5:
        shape = "J"

    return shape
